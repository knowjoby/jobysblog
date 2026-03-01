#!/usr/bin/env python3
"""
AI News Generator - Main script for fetching, scoring, and publishing AI news.
"""

import os
import sys
import json
import hashlib
import feedparser
import re
import yaml
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from difflib import SequenceMatcher
import html

# Import shared configuration
from scripts.config import (
    match_keywords,
    detect_companies,
    detect_topics,
    get_all_feeds,
    get_primary_feeds,
    COMPANY_KEYWORDS,
    TOPIC_KEYWORDS
)

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(__file__).parent.parent
POSTS_DIR = BASE_DIR / "_posts"
DATA_DIR = BASE_DIR / "_data"
QUEUE_FILE = DATA_DIR / "news_queue.json"
RUN_LOG_FILE = DATA_DIR / "run_log.json"
SOURCE_HEALTH_FILE = DATA_DIR / "source_health.yml"

# Ensure directories exist
POSTS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Scoring weights
SCORE_COMPANY_MENTION = 10      # Tier 1 company mention
SCORE_TIER2_COMPANY = 5         # Tier 2 company mention
SCORE_TOPIC_MATCH = 3           # Topic keyword match
SCORE_TITLE_BONUS = 8           # Company in title
SCORE_PRIMARY_SOURCE = 5        # From primary RSS feed
SCORE_COVERAGE_BONUS_2 = 8      # Covered by 2 sources
SCORE_COVERAGE_BONUS_3 = 15      # Covered by 3+ sources
SCORE_AGE_PENALTY_DAYS = 2      # Points deducted per day old
MAX_SCORE_AGE_DAYS = 7           # Max age before discard

# Post limits
DAILY_POST_LIMIT = 5
MIN_SCORE_TO_POST = 50
MAX_WORDS_PER_POST = 200

# Fallback settings
PRIMARY_FEED_NAMES = ["TechCrunch AI", "The Verge AI", "VentureBeat AI"]
MAX_CONSECUTIVE_FAILURES = 3


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def load_queue() -> Dict[str, Any]:
    """Load the news queue from JSON file."""
    if not QUEUE_FILE.exists():
        return {
            "queue": [],
            "config": {
                "daily_post_limit": DAILY_POST_LIMIT,
                "min_score_to_post": MIN_SCORE_TO_POST,
                "max_words_per_post": MAX_WORDS_PER_POST
            },
            "daily_usage": []
        }
    
    with open(QUEUE_FILE, 'r') as f:
        return json.load(f)


def save_queue(queue_data: Dict[str, Any]) -> None:
    """Save the news queue to JSON file."""
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue_data, f, indent=2)


def load_source_health() -> Dict[str, Any]:
    """Load source health tracking data."""
    if not SOURCE_HEALTH_FILE.exists():
        return {}
    
    with open(SOURCE_HEALTH_FILE, 'r') as f:
        return yaml.safe_load(f) or {}


def save_source_health(health_data: Dict[str, Any]) -> None:
    """Save source health tracking data."""
    with open(SOURCE_HEALTH_FILE, 'w') as f:
        yaml.dump(health_data, f, default_flow_style=False)


def append_to_run_log(entry: Dict[str, Any]) -> None:
    """Append an entry to the run log."""
    log_data = []
    if RUN_LOG_FILE.exists():
        with open(RUN_LOG_FILE, 'r') as f:
            try:
                log_data = json.load(f)
            except json.JSONDecodeError:
                log_data = []
    
    log_data.append(entry)
    
    # Keep only last 100 entries
    if len(log_data) > 100:
        log_data = log_data[-100:]
    
    with open(RUN_LOG_FILE, 'w') as f:
        json.dump(log_data, f, indent=2)


def titles_are_similar(title1: str, title2: str, threshold: float = 0.8) -> bool:
    """
    Check if two titles are similar enough to be considered the same story.
    """
    t1 = title1.lower().strip()
    t2 = title2.lower().strip()
    
    # Exact match
    if t1 == t2:
        return True
    
    # One contains the other with high overlap
    if len(t1) > len(t2):
        long, short = t1, t2
    else:
        long, short = t2, t1
    
    if short in long and len(short) > 15:
        return True
    
    # Fuzzy matching
    ratio = SequenceMatcher(None, t1, t2).ratio()
    return ratio > threshold


def clean_html(raw_html: str) -> str:
    """Remove HTML tags and clean text."""
    if not raw_html:
        return ""
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', raw_html)
    text = html.unescape(text)
    return ' '.join(text.split())


def get_item_hash(entry: Dict[str, Any]) -> str:
    """Generate a unique hash for a news item."""
    content = f"{entry['title']}{entry.get('source_url', '')}{entry.get('published', '')}"
    return hashlib.md5(content.encode()).hexdigest()[:12]


def get_post_filename(item: Dict[str, Any]) -> str:
    """Generate filename for a post."""
    date_str = datetime.now().strftime('%Y-%m-%d')
    title_slug = re.sub(r'[^\w\s-]', '', item['title'].lower())
    title_slug = re.sub(r'[-\s]+', '-', title_slug).strip('-')
    return f"{date_str}-{title_slug}.md"


def word_count(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def is_valid_item(entry: Dict[str, Any]) -> bool:
    """Validate that an item has required fields."""
    required = ['title', 'source_url', 'published']
    return all(entry.get(field) for field in required)


def get_age_days(published_str: str) -> float:
    """Calculate age of item in days."""
    try:
        # Try common RSS date formats
        for fmt in [
            '%a, %d %b %Y %H:%M:%S %z',
            '%a, %d %b %Y %H:%M:%S %Z',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%d %H:%M:%S',
        ]:
            try:
                pub_date = datetime.strptime(published_str, fmt)
                # Make timezone-aware if needed
                if pub_date.tzinfo is None:
                    pub_date = pub_date.replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                return (now - pub_date).total_seconds() / 86400
            except ValueError:
                continue
    except Exception:
        pass
    
    # Default to 0 if parsing fails (treat as fresh)
    return 0.0


def expand_age_cutoff(health_data: Dict[str, Any]) -> bool:
    """
    Check if all primary feeds have failed and we should expand age cutoff.
    """
    primary_failed = 0
    for feed_name in PRIMARY_FEED_NAMES:
        if feed_name in health_data:
            failures = health_data[feed_name].get('consecutive_failures', 0)
            if failures >= MAX_CONSECUTIVE_FAILURES:
                primary_failed += 1
    
    return primary_failed == len(PRIMARY_FEED_NAMES)


# =============================================================================
# SCORING FUNCTIONS
# =============================================================================

def score_item(
    item: Dict[str, Any],
    companies: List[str],
    topics: List[str],
    is_primary_source: bool = False
) -> int:
    """
    Calculate relevance score for a news item.
    """
    score = 0
    title = item.get('title', '')
    summary = item.get('summary', '')
    combined = f"{title} {summary}".lower()
    
    # Company mentions
    for company in companies:
        tier = 1 if company in [
            "openai", "anthropic", "google", "microsoft", "meta", "xai",
            "amazon", "apple", "nvidia"
        ] else 2
        
        if tier == 1:
            score += SCORE_COMPANY_MENTION
        else:
            score += SCORE_TIER2_COMPANY
        
        # Bonus if company in title
        if company in title.lower():
            score += SCORE_TITLE_BONUS
    
    # Topic matches
    for topic in topics:
        if topic in combined:
            score += SCORE_TOPIC_MATCH
    
    # Source quality bonus
    if is_primary_source:
        score += SCORE_PRIMARY_SOURCE
    
    # Age penalty
    age_days = get_age_days(item.get('published', ''))
    if age_days > MAX_SCORE_AGE_DAYS:
        return 0  # Too old, discard
    
    if age_days > 1:
        penalty = int(age_days * SCORE_AGE_PENALTY_DAYS)
        score -= penalty
    
    return max(0, score)


def apply_coverage_bonus(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Apply coverage bonus when multiple sources cover the same story.
    Modifies the list in place and returns it.
    """
    # First, group similar items
    grouped = []
    used_indices = set()
    
    for i, item in enumerate(candidates):
        if i in used_indices:
            continue
        
        similar_group = [item]
        used_indices.add(i)
        
        for j, other in enumerate(candidates[i+1:], i+1):
            if j in used_indices:
                continue
            
            if titles_are_similar(item['title'], other['title']):
                similar_group.append(other)
                used_indices.add(j)
        
        grouped.append(similar_group)
    
    # Now process each group
    result = []
    for group in grouped:
        if len(group) == 1:
            result.append(group[0])
            continue
        
        # Find the highest scoring item in the group
        best_item = max(group, key=lambda x: x['score'])
        
        # Apply coverage bonus
        if len(group) >= 3:
            bonus = SCORE_COVERAGE_BONUS_3
        else:
            bonus = SCORE_COVERAGE_BONUS_2
        
        best_item['score'] += bonus
        best_item['coverage_count'] = len(group)
        
        # Add sources from all group members
        all_sources = set()
        all_urls = set()
        for g in group:
            if 'source_name' in g:
                all_sources.add(g['source_name'])
            if 'source_url' in g:
                all_urls.add(g['source_url'])
        
        best_item['sources'] = list(all_sources)
        best_item['source_urls'] = list(all_urls)
        
        result.append(best_item)
    
    return result


# =============================================================================
# RSS FETCHING
# =============================================================================

def fetch_feed(feed_info: Dict[str, Any], health_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Fetch and parse a single RSS feed.
    Updates health tracking data.
    """
    feed_name = feed_info['name']
    feed_url = feed_info['url']
    is_primary = feed_info.get('primary', False)
    
    print(f"  Fetching {feed_name}...")
    
    # Initialize health entry if not exists
    if feed_name not in health_data:
        health_data[feed_name] = {
            'last_ok': None,
            'consecutive_failures': 0,
            'total_entries': 0,
            'last_entries': []
        }
    
    try:
        feed = feedparser.parse(feed_url)
        
        if feed.get('bozo_exception', 0):
            raise Exception(f"Feed parsing error: {feed.bozo_exception}")
        
        entries = []
        for entry in feed.entries[:20]:  # Limit to 20 per feed
            title = entry.get('title', '').strip()
            if not title:
                continue
            
            # Get summary/description
            summary = ''
            if hasattr(entry, 'summary'):
                summary = clean_html(entry.summary)
            elif hasattr(entry, 'description'):
                summary = clean_html(entry.description)
            
            # Get published date
            published = entry.get('published', '')
            if not published and hasattr(entry, 'updated'):
                published = entry.updated
            
            # Get link
            source_url = entry.get('link', '')
            
            item = {
                'title': title,
                'summary': summary[:500],  # Truncate
                'source_url': source_url,
                'published': published,
                'source_name': feed_name,
                'is_primary': is_primary,
                'age_days': get_age_days(published)
            }
            
            # Filter out items older than max age
            if item['age_days'] <= MAX_SCORE_AGE_DAYS:
                entries.append(item)
        
        # Update health tracking
        health_data[feed_name]['last_ok'] = datetime.now().isoformat()
        health_data[feed_name]['consecutive_failures'] = 0
        health_data[feed_name]['total_entries'] += len(entries)
        health_data[feed_name]['last_entries'] = [e['title'] for e in entries[:5]]
        
        print(f"    Found {len(entries)} valid entries")
        return entries
        
    except Exception as e:
        print(f"    ERROR: {e}")
        
        # Update failure tracking
        health_data[feed_name]['consecutive_failures'] += 1
        
        return []


def fetch_all_feeds() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Fetch all RSS feeds and return combined entries with health data.
    """
    health_data = load_source_health()
    all_entries = []
    
    feeds = get_all_feeds()
    print(f"Fetching {len(feeds)} RSS feeds...")
    
    for feed_info in feeds:
        entries = fetch_feed(feed_info, health_data)
        all_entries.extend(entries)
    
    # Save updated health data
    save_source_health(health_data)
    
    return all_entries, health_data


# =============================================================================
# POST GENERATION
# =============================================================================

def create_post_content(item: Dict[str, Any]) -> str:
    """
    Generate markdown content for a post.
    """
    # Prepare frontmatter
    frontmatter = {
        'layout': 'post',
        'title': item['title'],
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S %z'),
        'source': item.get('source_name', 'Unknown'),
        'source_url': item.get('source_url', '#'),
        'score': item['score'],
        'coverage_count': item.get('coverage_count', 1),
        'companies': item.get('companies', []),
        'topics': item.get('topics', [])
    }
    
    # Build content
    lines = ['---']
    for key, value in frontmatter.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for v in value:
                lines.append(f"  - {v}")
        else:
            lines.append(f"{key}: {value}")
    lines.append('---')
    lines.append('')
    
    # Add summary
    summary = item.get('summary', '')
    if summary:
        # Truncate to word limit
        words = summary.split()
        if len(words) > MAX_WORDS_PER_POST:
            summary = ' '.join(words[:MAX_WORDS_PER_POST]) + '...'
        lines.append(summary)
        lines.append('')
    
    # Add source attribution
    lines.append(f'<p><a href="{item["source_url"]}" target="_blank">Read original article</a></p>')
    
    # Add coverage info if multiple sources
    if item.get('coverage_count', 1) > 1:
        lines.append('')
        lines.append(f'*Covered by {item["coverage_count"]} sources*')
    
    return '\n'.join(lines)


def write_post(item: Dict[str, Any]) -> Optional[str]:
    """
    Write a post to file.
    Returns filename if successful, None otherwise.
    """
    filename = get_post_filename(item)
    filepath = POSTS_DIR / filename
    
    # Skip if already exists (avoid duplicates)
    if filepath.exists():
        print(f"  Post already exists: {filename}")
        return None
    
    content = create_post_content(item)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"  Created post: {filename}")
    return filename


def get_today_usage(queue_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get today's usage entry from queue data.
    """
    today = datetime.now().strftime('%Y-%m-%d')
    
    for usage in queue_data.get('daily_usage', []):
        if usage['date'] == today:
            return usage
    
    # Create new entry
    new_usage = {
        'date': today,
        'posts': 0,
        'items_processed': 0
    }
    queue_data.setdefault('daily_usage', []).append(new_usage)
    return new_usage


# =============================================================================
# MAIN PROCESS
# =============================================================================

def main():
    """Main execution function."""
    print(f"\n{'='*60}")
    print(f"AI News Generator - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")
    
    # Load queue data
    queue_data = load_queue()
    config = queue_data.get('config', {})
    daily_limit = config.get('daily_post_limit', DAILY_POST_LIMIT)
    min_score = config.get('min_score_to_post', MIN_SCORE_TO_POST)
    
    # Get today's usage
    today_usage = get_today_usage(queue_data)
    posts_today = today_usage.get('posts', 0)
    
    print(f"Posts today: {posts_today}/{daily_limit}")
    print(f"Min score required: {min_score}\n")
    
    # Check if we've hit the daily limit
    if posts_today >= daily_limit:
        print("Daily post limit reached. Exiting.")
        return
    
    # Fetch all feeds
    entries, health_data = fetch_all_feeds()
    print(f"\nTotal entries fetched: {len(entries)}")
    
    # Check if primary feeds failed and adjust age cutoff
    use_extended_age = expand_age_cutoff(health_data)
    if use_extended_age:
        print("WARNING: All primary feeds failing. Expanding age cutoff to 14 days.")
        global MAX_SCORE_AGE_DAYS
        MAX_SCORE_AGE_DAYS = 14
    
    # Process entries
    candidates = []
    for entry in entries:
        # Skip invalid items
        if not is_valid_item(entry):
            continue
        
        # Detect companies and topics
        combined_text = f"{entry['title']} {entry.get('summary', '')}"
        companies = detect_companies(combined_text)
        topics = detect_topics(combined_text)
        
        # Skip if no companies or topics found
        if not companies and not topics:
            continue
        
        # Calculate score
        score = score_item(
            entry, 
            companies, 
            topics, 
            is_primary_source=entry.get('is_primary', False)
        )
        
        # Skip low-scoring items
        if score < min_score:
            continue
        
        # Create candidate
        candidate = {
            'title': entry['title'],
            'summary': entry.get('summary', ''),
            'source_url': entry['source_url'],
            'published': entry['published'],
            'source_name': entry['source_name'],
            'companies': companies,
            'topics': topics,
            'score': score,
            'age_days': entry['age_days']
        }
        candidates.append(candidate)
    
    print(f"Candidates after scoring: {len(candidates)}")
    
    # Apply coverage bonus and deduplicate
    candidates = apply_coverage_bonus(candidates)
    print(f"After deduplication: {len(candidates)}")
    
    # Sort by score
    candidates.sort(key=lambda x: x['score'], reverse=True)
    
    # Determine how many posts to create
    posts_to_create = min(
        daily_limit - posts_today,
        len(candidates)
    )
    
    if posts_to_create == 0:
        print("No new posts to create.")
        return
    
    print(f"\nCreating {posts_to_create} posts...")
    
    # Create posts
    created_posts = []
    for i in range(posts_to_create):
        candidate = candidates[i]
        filename = write_post(candidate)
        if filename:
            created_posts.append({
                'title': candidate['title'],
                'filename': filename,
                'score': candidate['score'],
                'companies': candidate['companies']
            })
    
    # Update usage tracking
    today_usage['posts'] += len(created_posts)
    today_usage['items_processed'] += len(entries)
    
    # Save queue
    save_queue(queue_data)
    
    # Log this run
    run_entry = {
        'timestamp': datetime.now().isoformat(),
        'entries_fetched': len(entries),
        'candidates': len(candidates),
        'posts_created': len(created_posts),
        'primary_feeds_failing': use_extended_age
    }
    append_to_run_log(run_entry)
    
    print(f"\nDone! Created {len(created_posts)} posts.")
    
    # Check for breaking news
    if created_posts:
        try:
            from scripts.breaking_news_monitor import check_for_breaking_news
            breaking = check_for_breaking_news(created_posts)
            if breaking:
                print(f"Breaking news detected: {len(breaking)} items")
        except ImportError as e:
            print(f"Breaking news monitor not available: {e}")


if __name__ == "__main__":
    main()
