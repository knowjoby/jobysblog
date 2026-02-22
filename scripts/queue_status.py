#!/usr/bin/env python3
"""
AI News Queue Status
Usage: python scripts/queue_status.py [status|posted|pending|clear-old]
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

QUEUE = Path(__file__).parent.parent / "data" / "news_queue.json"


def load():
    with open(QUEUE) as f:
        return json.load(f)


def save(q):
    with open(QUEUE, "w") as f:
        json.dump(q, f, indent=2)


def status():
    q = load()
    today = datetime.now().strftime("%Y-%m-%d")
    cfg = q["config"]
    usage = q["daily_usage"].get(today, {"posts": 0, "estimated_tokens": 0})
    pending = sorted(q["pending"], key=lambda x: x.get("score", 0), reverse=True)
    recent = sorted(q["posted"], key=lambda x: x.get("posted_at", ""), reverse=True)

    posts_used = usage["posts"]
    posts_left = cfg["daily_post_limit"] - posts_used
    tokens_used = usage["estimated_tokens"]
    tokens_left = cfg["daily_token_budget"] - tokens_used
    token_pct = int(tokens_used / cfg["daily_token_budget"] * 100)

    print(f"\n{'='*50}")
    print(f"  AI News Queue — {today}")
    print(f"{'='*50}")
    print(f"  Posts today : {posts_used}/{cfg['daily_post_limit']}  ({posts_left} remaining)")
    print(f"  Tokens today: ~{tokens_used:,} / {cfg['daily_token_budget']:,}  ({token_pct}% used)")
    print(f"  Min score   : {cfg['min_score_to_post']}")

    print(f"\n  PENDING ({len(pending)} items):")
    if not pending:
        print("    — empty —")
    for i, item in enumerate(pending[:5], 1):
        companies = ", ".join(item.get("companies", []))
        topics = ", ".join(item.get("topics", []))
        print(f"    {i}. [{item.get('score', 0):3d}] {item['title']}")
        print(f"         {companies} | {topics} | added {item.get('added_at', '?')}")
    if len(pending) > 5:
        print(f"    ... and {len(pending) - 5} more")

    print(f"\n  RECENTLY POSTED:")
    if not recent:
        print("    — none yet —")
    for item in recent[:5]:
        companies = ", ".join(item.get("companies", []))
        print(f"    [{item.get('score', 0):3d}] {item.get('posted_at', '?')} — {item['title']}")
        print(f"         {companies} | {item.get('file', '')}")

    print(f"\n  TOTAL POSTED: {len(q['posted'])}")
    print(f"{'='*50}\n")


def clear_old(days=14):
    q = load()
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    before = len(q["pending"])
    q["pending"] = [p for p in q["pending"] if p.get("added_at", "9999") >= cutoff]
    removed = before - len(q["pending"])
    save(q)
    print(f"Removed {removed} pending items older than {days} days.")


def show_posted():
    q = load()
    recent = sorted(q["posted"], key=lambda x: x.get("posted_at", ""), reverse=True)
    print(f"\nAll posted ({len(recent)} total):\n")
    for item in recent:
        tags = ", ".join(item.get("companies", []) + item.get("topics", []))
        print(f"  [{item.get('score', 0):3d}] {item.get('posted_at', '?')} — {item['title']}")
        print(f"         tags: {tags}")
        print(f"         file: {item.get('file', 'unknown')}")
        print()


def show_pending():
    q = load()
    pending = sorted(q["pending"], key=lambda x: x.get("score", 0), reverse=True)
    print(f"\nPending queue ({len(pending)} items):\n")
    for i, item in enumerate(pending, 1):
        tags = ", ".join(item.get("companies", []) + item.get("topics", []))
        print(f"  {i}. [{item.get('score', 0):3d}] {item['title']}")
        print(f"       tags: {tags}")
        print(f"       added: {item.get('added_at', '?')} | source: {item.get('source_url', '')}")
        print()


COMMANDS = {
    "status": status,
    "posted": show_posted,
    "pending": show_pending,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "clear-old":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 14
        clear_old(days)
    elif cmd in COMMANDS:
        COMMANDS[cmd]()
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: queue_status.py [status|posted|pending|clear-old [days]]")
