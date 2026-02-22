#!/usr/bin/env python3
"""
AI news link-post generator for Jekyll blog.
No API key needed — pulls from RSS feeds, scores by keyword rules,
saves minimal link posts (title + URL + tags).

Requires: pip install feedparser
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

import feedparser

REPO_ROOT  = Path(__file__).parent.parent
QUEUE_FILE = REPO_ROOT / "data" / "news_queue.json"
LOG_FILE   = REPO_ROOT / "_data" / "run_log.json"
POSTS_DIR  = REPO_ROOT / "_posts"

RSS_FEEDS = [
    # --- Tech media ---
    ("TechCrunch",      "https://techcrunch.com/feed/"),
    ("The Verge",       "https://www.theverge.com/rss/index.xml"),
    ("VentureBeat",     "https://feeds.feedburner.com/venturebeat/SZYF"),
    ("Ars Technica",    "https://feeds.arstechnica.com/arstechnica/index"),
    ("Wired",           "https://www.wired.com/feed/rss"),
    ("MIT Tech Review", "https://www.technologyreview.com/feed/"),
    ("CNBC Tech",       "https://www.cnbc.com/id/19854910/device/rss/rss.html"),

    # --- Company blogs (first-party, no RSS: Anthropic, DeepMind, Meta AI) ---
    ("OpenAI",          "https://openai.com/news/rss.xml"),
    ("Google AI",       "https://blog.google/technology/ai/rss/"),
    ("Microsoft AI",    "https://blogs.microsoft.com/ai/feed/"),
    ("Hugging Face",    "https://huggingface.co/blog/feed.xml"),

    # --- AI-specialist newsletters ---
    ("Import AI",       "https://importai.substack.com/feed"),
    ("Platformer",      "https://www.platformer.news/rss/"),
]

# --- Keyword maps for auto-tagging and scoring ---

COMPANY_KEYWORDS = {
    "anthropic":  ["anthropic", "claude"],
    "openai":     ["openai", "chatgpt", "gpt-", "sora"],
    "google":     ["google", "deepmind", "gemini", "bard"],
    "microsoft":  ["microsoft", "copilot", "azure ai", "bing ai"],
    "meta":       ["meta ai", "llama", " meta "],
    "xai":        ["xai", "grok", "elon musk ai"],
    "mistral":    ["mistral"],
    "cohere":     ["cohere"],
    "apple":      ["apple intelligence", "apple ai"],
    "amazon":     ["amazon ai", "aws ai", "alexa ai", "bedrock"],
    "nvidia":     ["nvidia", "cuda ai"],
}

TOPIC_KEYWORDS = {
    "release":      ["launch", "release", "announce", "unveil", "introduce", "debut", "ship"],
    "controversy":  ["controversy", "backlash", "criticize", "outrage", "anger", "fired", "resign"],
    "product":      ["product", "feature", "update", "integrat", "app", "tool", "platform"],
    "bug":          ["bug", "outage", "down", "fail", "error", "glitch", "crash", "breach"],
    "rumor":        ["rumor", "reportedly", "leak", "unconfirmed", "said to"],
    "funding":      ["funding", "raises", "valuation", "billion", "invest", "series"],
    "partnership":  ["partner", "deal", "agreement", "collaborat"],
    "policy":       ["policy", "regulation", "law", "ban", "congress", "eu ai", "govern"],
    "safety":       ["safety", "alignment", "harm", "risk", "dangerous", "red line", "bias"],
    "benchmark":    ["benchmark", "beats", "outperform", "state-of-the-art", "sota"],
    "agentic":      ["agent", "agentic", "autonomous", "automat"],
    "multimodal":   ["multimodal", "vision", "image", "video", "audio"],
    "drama":        ["drama", "feud", "clash", "tension", "fight", "dispute"],
}


def slugify(text):
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return re.sub(r"-+", "-", s)[:55]


def detect_companies(text):
    t = text.lower()
    return [co for co, kws in COMPANY_KEYWORDS.items() if any(k in t for k in kws)]


def detect_topics(text):
    t = text.lower()
    topics = [tp for tp, kws in TOPIC_KEYWORDS.items() if any(k in t for k in kws)]
    if "rumor" in topics and "unverified" not in topics:
        topics.append("unverified")
    return topics


STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "in", "on", "at", "to",
    "for", "of", "and", "or", "with", "by", "its", "it", "as", "from",
    "that", "this", "has", "have", "new", "says", "say", "over", "after",
    "how", "why", "what", "will", "can", "be", "been", "but", "not", "no",
}

def titles_are_similar(t1, t2, threshold=0.45):
    """Return True if two titles are likely covering the same story."""
    w1 = set(re.sub(r"[^a-z0-9\s]", "", t1.lower()).split()) - STOP_WORDS
    w2 = set(re.sub(r"[^a-z0-9\s]", "", t2.lower()).split()) - STOP_WORDS
    if len(w1) < 3 or len(w2) < 3:
        return False
    union = len(w1 | w2)
    return len(w1 & w2) / union >= threshold


def parse_date(entry):
    for field in ("published_parsed", "updated_parsed"):
        val = entry.get(field)
        if val:
            return datetime(*val[:6], tzinfo=timezone.utc)
    for field in ("published", "updated"):
        val = entry.get(field, "")
        if val:
            try:
                return parsedate_to_datetime(val).astimezone(timezone.utc)
            except Exception:
                pass
    return datetime.now(timezone.utc)


def score_item(title, companies, topics, pub_date, existing_titles):
    now = datetime.now(timezone.utc)
    age_days = (now - pub_date).days

    # Recency (0-25)
    if age_days == 0:    recency = 25
    elif age_days <= 2:  recency = 18
    elif age_days <= 5:  recency = 12
    elif age_days <= 7:  recency = 6
    else:                recency = 2

    # Company tier (0-25)
    tier1 = {"anthropic", "openai", "google", "microsoft"}
    tier2 = {"meta", "xai", "apple", "amazon", "nvidia"}
    if any(c in tier1 for c in companies):   company_score = 25
    elif any(c in tier2 for c in companies): company_score = 18
    elif companies:                          company_score = 10
    else:                                    company_score = 0

    # Topic importance (0-30)
    weights = {
        "safety": 30, "controversy": 28, "drama": 25,
        "release": 22, "product": 18, "benchmark": 16,
        "funding": 14, "partnership": 12, "policy": 12,
        "agentic": 10, "multimodal": 10, "bug": 10,
        "rumor": 8,
    }
    topic_score = max((weights.get(t, 5) for t in topics), default=5)

    # Uniqueness (0-20): penalise if title too similar to existing
    title_l = title.lower()
    if any(title_l in e.lower() or e.lower() in title_l for e in existing_titles):
        uniqueness = 0
    elif any(
        any(c in e.lower() for c in companies) and
        any(t in e.lower() for t in topics)
        for e in existing_titles
    ):
        uniqueness = 10
    else:
        uniqueness = 20

    return recency + company_score + topic_score + uniqueness


def load_queue():
    with open(QUEUE_FILE) as f:
        return json.load(f)


def save_queue(q):
    with open(QUEUE_FILE, "w") as f:
        json.dump(q, f, indent=2)


def write_run_log(candidates_found, posts_written, queued_count):
    event = os.environ.get("GITHUB_EVENT_NAME", "")
    if event == "schedule":
        triggered_by = "Scheduled (daily)"
    elif event == "workflow_dispatch":
        triggered_by = "Manual (GitHub)"
    else:
        triggered_by = "Manual (local)"

    entry = {
        "ran_at":            datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d %H:%M:%S IST"),
        "triggered_by":      triggered_by,
        "candidates_found":  candidates_found,
        "posts_created":     len(posts_written),
        "queued":            queued_count,
        "posts": [
            {
                "title": p["title"],
                "file":  p["file"],
                "score": p["score"],
                "tags":  p["companies"] + p["topics"],
            }
            for p in posts_written
        ],
    }

    log = []
    if LOG_FILE.exists():
        try:
            log = json.loads(LOG_FILE.read_text())
        except Exception:
            log = []

    log.append(entry)
    log = log[-50:]  # keep last 50 runs
    LOG_FILE.write_text(json.dumps(log, indent=2))


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    queue = load_queue()
    config = queue["config"]
    usage = queue["daily_usage"].get(today, {"posts": 0, "estimated_tokens": 0})
    posts_remaining = config["daily_post_limit"] - usage["posts"]

    if posts_remaining <= 0:
        print(f"Daily post limit reached ({config['daily_post_limit']}). Nothing to do.")
        write_run_log(0, [], 0)
        return

    existing_titles = [p.get("title", "") for p in queue["posted"] + queue["pending"]]
    existing_urls   = {p.get("source_url", "") for p in queue["posted"] + queue["pending"]}

    # Collect and score candidates from RSS
    candidates = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)

    for source_name, feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            print(f"Feed error ({feed_url}): {e}", file=sys.stderr)
            continue

        for entry in feed.entries[:25]:
            title   = entry.get("title", "").strip()
            url     = entry.get("link", "").strip()
            summary = re.sub(r"<[^>]+>", "", entry.get("summary", ""))
            pub     = parse_date(entry)

            if not title or not url:
                continue
            if url in existing_urls:
                continue
            if pub < cutoff:
                continue

            text      = title + " " + summary
            companies = detect_companies(text)
            topics    = detect_topics(text)

            # Must mention an AI company or have a strong AI topic
            if not companies and not any(t in topics for t in ("release", "safety", "policy", "agentic")):
                ai_generic = ["artificial intelligence", "ai model", "large language model", "llm", "generative ai"]
                if not any(kw in text.lower() for kw in ai_generic):
                    continue

            s = score_item(title, companies, topics, pub, existing_titles)
            if s < 10:
                continue

            candidates.append({
                "title":      title,
                "url":        url,
                "source":     source_name,
                "companies":  companies,
                "topics":     topics,
                "score":      s,
                "pub_date":   pub.strftime("%Y-%m-%d"),
            })

    if not candidates:
        print("No new AI news items found.")
        return

    # Deduplicate: same story covered by multiple outlets — keep highest scored
    deduped = []
    for item in candidates:
        matched = next(
            (kept for kept in deduped if titles_are_similar(item["title"], kept["title"])),
            None,
        )
        if matched is None:
            deduped.append(item)
        elif item["score"] > matched["score"]:
            deduped[deduped.index(matched)] = item  # upgrade to better-scored version

    dupes_removed = len(candidates) - len(deduped)
    candidates = deduped

    candidates.sort(key=lambda x: x["score"], reverse=True)
    print(f"Found {len(candidates)} candidate(s) ({dupes_removed} cross-source duplicate(s) removed)")

    # Write top N posts (max 5/day total, max 2/day per company)
    posts_written = []
    company_counts = {}
    PER_COMPANY_LIMIT = 2
    for item in candidates:
        if len(posts_written) >= posts_remaining:
            break
        if item["score"] < config["min_score_to_post"]:
            break
        # Skip if any company in this item has hit its per-company cap
        if item["companies"] and all(
            company_counts.get(co, 0) >= PER_COMPANY_LIMIT for co in item["companies"]
        ):
            continue

        slug     = slugify(item["title"])
        filename = f"{today}-{slug}.md"
        filepath = POSTS_DIR / filename
        if filepath.exists():
            continue

        tags     = item["companies"] + item["topics"]
        now_str  = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
        safe_title = item["title"].replace('"', "'")

        content = (
            f"---\n"
            f'layout: post\n'
            f'title: "{safe_title}"\n'
            f'date: {now_str}\n'
            f'categories: ai-news\n'
            f'tags: [{", ".join(tags)}]\n'
            f'score: {item["score"]}\n'
            f'link: {item["url"]}\n'
            f'source: {item["source"]}\n'
            f'original_date: {item["pub_date"]}\n'
            f'---\n\n'
            f'[Read on {item["source"]}]({item["url"]})\n'
        )
        filepath.write_text(content)
        print(f"  [{item['score']:3d}] {filename}")

        entry_data = {
            "id":         f"{slug}-{today}",
            "title":      item["title"],
            "source_url": item["url"],
            "companies":  item["companies"],
            "topics":     item["topics"],
            "score":      item["score"],
            "file":       f"_posts/{filename}",
            "added_at":   today,
            "posted_at":  today,
        }
        queue["posted"].append(entry_data)
        existing_urls.add(item["url"])
        posts_written.append(entry_data)
        for co in item["companies"]:
            company_counts[co] = company_counts.get(co, 0) + 1

    # Queue remaining good candidates for future days
    for item in candidates[len(posts_written):len(posts_written) + 10]:
        if item["score"] < 40:
            break
        if item["url"] in existing_urls:
            continue
        queue["pending"].append({
            "id":         f"{slugify(item['title'])}-{today}",
            "title":      item["title"],
            "source_url": item["url"],
            "companies":  item["companies"],
            "topics":     item["topics"],
            "score":      item["score"],
            "added_at":   today,
        })
        existing_urls.add(item["url"])

    queue["pending"].sort(key=lambda x: x.get("score", 0), reverse=True)
    # Drop pending older than 14 days
    old_cutoff = (datetime.now(timezone.utc) - timedelta(days=14)).strftime("%Y-%m-%d")
    queue["pending"] = [p for p in queue["pending"] if p.get("added_at", "9999") >= old_cutoff]

    queue["daily_usage"][today] = {
        "posts":             usage["posts"] + len(posts_written),
        "estimated_tokens":  0,  # no API calls
    }
    save_queue(queue)

    write_run_log(len(candidates), posts_written, len(new_pending))
    print(f"\nDone: {len(posts_written)} post(s) written, {len(queue['pending'])} item(s) in queue")


if __name__ == "__main__":
    main()
