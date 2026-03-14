#!/usr/bin/env python3
"""
Daily AI PM blog post generator.
Uses GitHub Models (Phi-3.5-mini) via the OpenAI-compatible API.
Runs in GitHub Actions — uses GITHUB_TOKEN for auth.
"""

import os
import json
import datetime
import re
import sys
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("openai package not found. Run: pip install openai")
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
QUEUE_FILE = REPO_ROOT / "data" / "topics_queue.json"
POSTS_DIR = REPO_ROOT / "_posts"

MODEL = "microsoft/Phi-3.5-mini-instruct"
MAX_WORDS = 480  # stay under 500


def load_queue():
    with open(QUEUE_FILE) as f:
        return json.load(f)


def save_queue(queue):
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)


def get_next_topic(queue):
    topics = queue["topics"]
    idx = queue.get("current_index", 0)
    # Find next pending topic starting from current index
    for i in range(len(topics)):
        pos = (idx + i) % len(topics)
        if topics[pos]["status"] == "pending":
            return pos, topics[pos]
    # All done — reset and start over
    for t in topics:
        t["status"] = "pending"
    queue["current_index"] = 0
    save_queue(queue)
    return 0, topics[0]


def slugify(title):
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug[:60]


def level_description(level):
    return {
        "beginner": "a Product Manager who is new to AI/ML products (0-12 months experience)",
        "advanced": "an experienced Product Manager with 1-2 years of AI product experience",
        "expert": "a senior Product Manager or AI product leader managing AI at scale",
    }.get(level, "a Product Manager")


def generate_post(topic, client):
    level = topic["level"]
    title = topic["title"]
    audience = level_description(level)

    prompt = f"""Write a blog post for {audience}.

Title: {title}

Requirements:
- Under {MAX_WORDS} words total
- Practical and actionable — no fluff
- Use 2-3 short sections with ## headers
- Write in a direct, confident tone (like a senior PM explaining to a peer)
- End with one concrete takeaway or action item
- Do NOT include the title in the body (it will be added from front matter)
- Do NOT add a preamble like "Here is the post:" — start directly with the first section

Write the post now:"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an expert AI Product Management coach. You write clear, concise blog posts for product managers. Your writing is practical, no-nonsense, and under 500 words.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=800,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()


def build_front_matter(title, level, date_str):
    tags_map = {
        "beginner": ["beginner", "foundations"],
        "advanced": ["advanced", "strategy"],
        "expert": ["expert", "leadership"],
    }
    tags = tags_map.get(level, ["general"])
    tags_str = "[" + ", ".join(tags) + "]"

    return f"""---
layout: post
title: "{title}"
date: {date_str} 08:00:00 +0000
categories: ai-pm
tags: {tags_str}
level: {level}
---
"""


def already_posted_today(queue):
    today = datetime.date.today().isoformat()
    return queue.get("last_post_date") == today


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not set")
        sys.exit(1)

    queue = load_queue()

    if already_posted_today(queue):
        print("Already posted today. Skipping.")
        sys.exit(0)

    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=token,
    )

    idx, topic = get_next_topic(queue)
    print(f"Generating post: [{topic['level']}] {topic['title']}")

    content = generate_post(topic, client)

    today = datetime.date.today().isoformat()
    slug = slugify(topic["title"])
    filename = f"{today}-{slug}.md"
    filepath = POSTS_DIR / filename

    front_matter = build_front_matter(topic["title"], topic["level"], today)
    full_post = front_matter + "\n" + content + "\n"

    filepath.write_text(full_post)
    print(f"Wrote: {filepath}")

    # Update queue
    queue["topics"][idx]["status"] = "posted"
    queue["current_index"] = (idx + 1) % len(queue["topics"])
    queue["last_post_date"] = today
    save_queue(queue)
    print("Queue updated.")


if __name__ == "__main__":
    main()
