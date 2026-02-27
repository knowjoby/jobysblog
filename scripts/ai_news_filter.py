# scripts/ai_news_filter.py
import feedparser
import re
from datetime import datetime
import yaml
from pathlib import Path
import logging

# Configure your target companies and keywords
COMPANY_KEYWORDS = {
    'openai': ['openai', 'chatgpt', 'gpt-4', 'o1', 'sora', 'dall-e'],
    'anthropic': ['anthropic', 'claude', 'claude 3', 'constitutional ai'],
    'google': ['google ai', 'gemini', 'deepmind', 'bard', 'palm 2'],
    'deepseek': ['deepseek', 'deep seek'],
    'microsoft': ['microsoft ai', 'copilot', 'azure ai'],
    'meta': ['meta ai', 'llama', 'llama 3'],
}

# Your expanded source list
SOURCES = [
    # Substack newsletters
    {'name': 'Import AI', 'url': 'https://importai.substack.com/feed'},
    {'name': 'The Algorithm', 'url': 'https://www.thealgorithm.tech/feed'},
    {'name': 'AI Snake Oil', 'url': 'https://aisnakeoil.substack.com/feed'},
    {'name': 'Latent Space', 'url': 'https://latent.space/feed'},
    {'name': 'Interconnects', 'url': 'https://www.interconnects.ai/feed'},
    
    # Company blogs
    {'name': 'OpenAI Blog', 'url': 'https://openai.com/blog/rss/'},
    {'name': 'Anthropic News', 'url': 'https://www.anthropic.com/news/rss.xml'},
    {'name': 'Google AI Blog', 'url': 'http://feeds.feedburner.com/blogspot/gJZg'},
    {'name': 'DeepMind Blog', 'url': 'https://deepmind.google/blog/rss/'},
    
    # Tech publications
    {'name': 'TechCrunch AI', 'url': 'https://techcrunch.com/category/artificial-intelligence/feed/'},
    {'name': 'VentureBeat AI', 'url': 'https://venturebeat.com/category/ai/feed/'},
    {'name': 'Wired AI', 'url': 'https://www.wired.com/feed/tag/ai/latest/rss'},
]

def extract_companies_mentioned(text, title):
    """
    Check if content mentions target companies.
    Returns dict of companies found and their relevance score.
    """
    combined_text = f"{title} {text}".lower()
    mentioned = {}
    
    for company, keywords in COMPANY_KEYWORDS.items():
        # Count keyword occurrences for relevance scoring
        score = sum(combined_text.count(keyword) for keyword in keywords)
        if score > 0:
            # Check if it's a significant mention (more than just passing)
            is_significant = score > 1 or any(
                re.search(rf'\b{keyword}\b', combined_text) 
                for keyword in keywords[:2]  # Check primary keywords
            )
            mentioned[company] = {
                'score': score,
                'primary': is_significant
            }
    
    return mentioned

def update_source_health(name, success=True):
    """Stub for source health tracking — not yet implemented."""
    pass


def fetch_and_filter_news():
    """
    Main function to fetch, filter, and save news.
    """
    all_posts = []
    
    for source in SOURCES:
        try:
            feed = feedparser.parse(source['url'])
            
            for entry in feed.entries[:10]:  # Last 10 items per source
                # Extract content
                content = entry.get('summary', '') or entry.get('description', '')
                if hasattr(entry, 'content'):
                    content = entry.content[0].value
                
                # Check for company mentions
                companies = extract_companies_mentioned(content, entry.title)
                
                if companies:
                    # Create post with enhanced metadata
                    post = {
                        'title': entry.title,
                        'link': entry.link,
                        'date': datetime(*entry.published_parsed[:6]),
                        'source': source['name'],
                        'summary': content[:500] + '...' if len(content) > 500 else content,
                        'companies': companies,
                        'primary_company': max(companies.items(), 
                                             key=lambda x: x[1]['score'])[0],
                        'relevance_score': sum(c['score'] for c in companies.values()),
                    }
                    all_posts.append(post)
                    
                    logging.info(f"✅ Found: {entry.title} (mentions: {', '.join(companies.keys())})")
                else:
                    logging.debug(f"⏭️  Skipped: {entry.title} - no company mentions")
                    
        except Exception as e:
            logging.error(f"❌ Error fetching {source['name']}: {e}")
            # Update your health tracking
            update_source_health(source['name'], success=False)
    
    # Sort by date and relevance
    all_posts.sort(key=lambda x: (x['date'], x['relevance_score']), reverse=True)
    
    # Save to your data structure
    save_filtered_news(all_posts)
    
    return all_posts

def save_filtered_news(posts):
    """
    Save posts in your existing format.
    Creates dated files in /_posts and updates /_data.
    """
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Save as individual posts (your existing format)
    for i, post in enumerate(posts[:20]):  # Top 20 most relevant
        post_file = Path(f'_posts/{today}-ai-news-{i+1}.md')
        post_content = f"""---
layout: post
title: "{post['title']}"
date: {post['date'].strftime('%Y-%m-%d %H:%M:%S')}
source: {post['source']}
companies: {', '.join(post['companies'].keys())}
primary: {post['primary_company']}
link: {post['link']}
---

{post['summary']}

[Read full article]({post['link']}) | via {post['source']}
"""
        post_file.write_text(post_content)
    
    # Update your data file for the homepage
    data_file = Path(f'_data/ai-news-{today}.yaml')
    yaml.dump(posts[:50], data_file.open('w'))

# Add to your existing workflow
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    news = fetch_and_filter_news()
    print(f"Found {len(news)} relevant AI news items")
