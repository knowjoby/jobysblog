#!/usr/bin/env python3
"""
Queue Status - CLI tool to inspect the news queue and daily usage.
"""

import sys
from pathlib import Path
# Add repo root to path for imports (though this script doesn't import from config)
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from datetime import datetime
from typing import Dict, Any, Optional

BASE_DIR = Path(__file__).parent.parent
QUEUE_FILE = BASE_DIR / "data" / "news_queue.json"
RUN_LOG_FILE = BASE_DIR / "_data" / "run_log.json"


def load_queue() -> Dict[str, Any]:
    """Load the news queue from JSON file."""
    if not QUEUE_FILE.exists():
        return {"queue": [], "config": {}, "daily_usage": []}
    
    with open(QUEUE_FILE, 'r') as f:
        return json.load(f)


def load_run_log() -> list:
    """Load the run log."""
    if not RUN_LOG_FILE.exists():
        return []
    
    with open(RUN_LOG_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}")


def show_config(config: Dict[str, Any]) -> None:
    """Display current configuration."""
    print_header("CONFIGURATION")
    for key, value in config.items():
        print(f"  {key}: {value}")


def show_daily_usage(usage_list: list) -> None:
    """Display daily usage statistics."""
    print_header("DAILY USAGE")
    
    if not usage_list:
        print("  No usage data")
        return
    
    # Sort by date descending
    usage_list = sorted(usage_list, key=lambda x: x.get('date', ''), reverse=True)
    
    for usage in usage_list[:10]:  # Show last 10 days
        date = usage.get('date', 'unknown')
        posts = usage.get('posts', 0)
        processed = usage.get('items_processed', 0)
        print(f"  {date}: {posts} posts from {processed} items")


def show_queue(queue: list, limit: int = 10) -> None:
    """Display current queue items."""
    print_header(f"QUEUE (showing top {limit})")
    
    if not queue:
        print("  Queue is empty")
        return
    
    # Sort by score descending
    queue = sorted(queue, key=lambda x: x.get('score', 0), reverse=True)
    
    for i, item in enumerate(queue[:limit]):
        score = item.get('score', 0)
        title = item.get('title', 'Untitled')
        companies = item.get('companies', [])
        print(f"  {i+1:2d}. [{score:3d}] {title[:60]}")
        if companies:
            print(f"      Companies: {', '.join(companies)}")


def show_recent_runs(run_log: list, limit: int = 5) -> None:
    """Display recent run log entries."""
    print_header("RECENT RUNS")
    
    if not run_log:
        print("  No run data")
        return
    
    for entry in run_log[-limit:]:
        timestamp = entry.get('timestamp', '')[:19]  # Truncate to YYYY-MM-DD HH:MM:SS
        fetched = entry.get('entries_fetched', 0)
        candidates = entry.get('candidates', 0)
        posts = entry.get('posts_created', 0)
        failing = entry.get('primary_feeds_failing', False)
        
        status = "⚠️" if failing else "✓"
        print(f"  {status} {timestamp} - Fetched: {fetched}, Candidates: {candidates}, Posts: {posts}")


def show_breaking_news(run_log: list, limit: int = 5) -> None:
    """Show recent breaking news from run log."""
    print_header("RECENT BREAKING NEWS")
    
    breaking_entries = [
        e for e in run_log 
        if isinstance(e, dict) and e.get('type') == 'breaking_news'
    ]
    
    if not breaking_entries:
        print("  No breaking news
