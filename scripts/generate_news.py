#!/usr/bin/env python3
"""
Automated AI news generator for Jekyll blog.
Runs via GitHub Actions daily or on manual trigger.
Requires: pip install anthropic feedparser
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import anthropic
import feedparser

REPO_ROOT = Path(__file__).parent.parent
QUEUE_FILE = REPO_ROOT / "data" / "news_queue.json"
POSTS_DIR = REPO_ROOT / "_posts"

RSS_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://venturebeat.com/feed/",
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://www.wired.com/feed/rss",
    "https://www.reuters.com/technology/artificial-intelligence/rss/",
]

AI_KEYWORDS = [
    "openai", "anthropic", "claude", "chatgpt", "gpt", "gemini",
    "copilot", "large language model", "llm", "deepmind", "meta ai",
    "llama", "grok", "xai", "mistral", "cohere", "ai model",
    "artificial intelligence", "generative ai", "foundation model",
    "nvidia", "microsoft ai", "google ai",
]


def load_queue():
    with open(QUEUE_FILE) as f:
        return json.load(f)


def save_queue(q):
    with open(QUEUE_FILE, "w") as f:
        json.dump(q, f, indent=2)


def slugify(text):
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s[:50]


def fetch_rss_items():
    items = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            source_name = feed.feed.get("title", url)
            for entry in feed.entries[:20]:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                link = entry.get("link", "")
                published = entry.get("published", "")
                text = (title + " " + summary).lower()
                if any(kw in text for kw in AI_KEYWORDS):
                    items.append({
                        "title": title,
                        "summary": re.sub(r"<[^>]+>", "", summary)[:600],
                        "url": link,
                        "published": published,
                        "source": source_name,
                    })
        except Exception as e:
            print(f"Feed error ({url}): {e}", file=sys.stderr)
    return items


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    queue = load_queue()
    config = queue["config"]
    usage = queue["daily_usage"].get(today, {"posts": 0, "estimated_tokens": 0})
    posts_remaining = config["daily_post_limit"] - usage["posts"]

    if posts_remaining <= 0:
        print(f"Daily post limit reached ({config['daily_post_limit']}). Nothing to do.")
        return

    print("Fetching RSS feeds...")
    items = fetch_rss_items()
    print(f"Found {len(items)} AI-related items")

    if not items:
        print("No items found. Exiting.")
        return

    existing = [p.get("title", "") for p in queue["posted"] + queue["pending"]]
    existing_titles = "\n".join(f"- {t}" for t in existing[-30:]) or "None"
    items_text = "\n\n".join(
        f"ITEM {i+1}:\nTitle: {item['title']}\nSource: {item['source']}\n"
        f"Published: {item['published']}\nURL: {item['url']}\nSummary: {item['summary']}"
        for i, item in enumerate(items[:30])
    )

    prompt = f"""You are an AI news curator for a personal blog. Today is {today}.

Here are recent AI-related news items from RSS feeds:

{items_text}

Already posted or queued (avoid duplicates on the same story):
{existing_titles}

Instructions:
1. Score each ITEM 0-100:
   - Recency (0-25): published today=25, 1-2 days=18, 3-5 days=12, older=5
   - Company tier (0-25): Anthropic/OpenAI/Google DeepMind/Microsoft=25, Meta/xAI/Apple/Nvidia=18, others=10
   - Topic importance (0-30): safety incident or controversy=30, major model release=25, significant product=20, funding or partnership=15, rumor or leak=10, minor update=5
   - Uniqueness (0-20): no similar story in existing list=20, same company different topic=10, too similar=0

2. Select the top {posts_remaining} item(s) with score >= {config['min_score_to_post']} to POST TODAY.
   Also pick up to 5 others for the queue (future days).

3. For each item to post, write a 150-200 word article:
   - Open with the fact: what happened, who, when
   - Why it matters (1-2 sentences)
   - What to watch next (1 sentence if relevant)
   - Last line: **Source:** [Publication Name](url)
   - Tone: factual, neutral, no hype
   - If rumor or unverified: say so inline ("reportedly", "according to unverified reports")

4. Tags — use ONLY from these lists:
   Company: anthropic openai microsoft google meta xai mistral cohere apple amazon nvidia
   Topic: release controversy product bug rumor funding partnership policy safety unverified drama benchmark agentic multimodal
   Rumors always get both "rumor" AND "unverified" tags.

Respond ONLY with valid JSON, no markdown code fences:
{{
  "to_post": [
    {{
      "title": "...",
      "slug": "3-to-5-word-slug",
      "companies": ["anthropic"],
      "topics": ["controversy"],
      "score": 82,
      "source_url": "...",
      "body": "Article body 150-200 words. Plain markdown. No front matter.\\n\\n**Source:** [Name](url)"
    }}
  ],
  "to_queue": [
    {{
      "title": "...",
      "summary": "One sentence summary.",
      "source_url": "...",
      "companies": ["openai"],
      "topics": ["release"],
      "score": 65
    }}
  ]
}}"""

    client = anthropic.Anthropic()
    print("Calling Claude API...")
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    raw = re.sub(r"^```(?:json)?\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}\nResponse preview: {raw[:500]}", file=sys.stderr)
        sys.exit(1)

    existing_lower = [t.lower() for t in existing]
    posts_written = []

    for item in result.get("to_post", []):
        title = item["title"]
        if any(title.lower() in e or e in title.lower() for e in existing_lower):
            print(f"Skipping duplicate: {title}")
            continue

        slug = slugify(item.get("slug", title))
        filename = f"{today}-{slug}.md"
        filepath = POSTS_DIR / filename

        if filepath.exists():
            print(f"File exists, skipping: {filename}")
            continue

        tags = item.get("companies", []) + item.get("topics", [])
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
        content = (
            f"---\n"
            f"layout: post\n"
            f"title: \"{title.replace(chr(34), chr(39))}\"\n"
            f"date: {now}\n"
            f"categories: ai-news\n"
            f"tags: [{', '.join(tags)}]\n"
            f"score: {item.get('score', 0)}\n"
            f"---\n\n"
            f"{item['body']}\n"
        )
        filepath.write_text(content)
        print(f"Written: {filename}")

        posts_written.append({
            "id": f"{slug}-{today}",
            "title": title,
            "summary": item.get("body", "")[:150],
            "source_url": item.get("source_url", ""),
            "companies": item.get("companies", []),
            "topics": item.get("topics", []),
            "score": item.get("score", 0),
            "file": f"_posts/{filename}",
            "added_at": today,
            "posted_at": today,
        })

    existing_urls = {p.get("source_url") for p in queue["posted"] + queue["pending"]}
    new_pending = []
    for item in result.get("to_queue", []):
        if item.get("source_url") in existing_urls:
            continue
        new_pending.append({
            "id": f"{slugify(item['title'])}-{today}",
            "title": item["title"],
            "summary": item.get("summary", ""),
            "source_url": item.get("source_url", ""),
            "companies": item.get("companies", []),
            "topics": item.get("topics", []),
            "score": item.get("score", 0),
            "added_at": today,
        })

    queue["posted"].extend(posts_written)
    queue["pending"].extend(new_pending)
    queue["pending"].sort(key=lambda x: x.get("score", 0), reverse=True)

    cutoff = (datetime.now(timezone.utc) - timedelta(days=14)).strftime("%Y-%m-%d")
    queue["pending"] = [p for p in queue["pending"] if p.get("added_at", "9999") >= cutoff]

    tokens_used = response.usage.input_tokens + response.usage.output_tokens
    queue["daily_usage"][today] = {
        "posts": usage["posts"] + len(posts_written),
        "estimated_tokens": usage["estimated_tokens"] + tokens_used,
    }
    save_queue(queue)

    print(f"\nDone: {len(posts_written)} post(s) written, {len(new_pending)} item(s) queued")
    for p in posts_written:
        print(f"  [{p['score']}] {p['title']}")


if __name__ == "__main__":
    main()
