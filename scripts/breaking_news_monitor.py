# scripts/breaking_news_monitor.py

import json
from pathlib import Path
import smtplib
import requests
from datetime import datetime

class BreakingNewsMonitor:
    def __init__(self):
        self.cache_file = Path('data/breaking_news_cache.json')
        self.load_cache()
        
        # Define what constitutes "breaking news"
        self.BREAKING_KEYWORDS = [
            'just released', 'announces', 'launches', 'unveils',
            'GPT-5', 'Claude 4', 'Gemini Ultra', 'breakthrough',
            'major update', 'acquisition', 'partnership'
        ]
        
        # Companies that trigger immediate attention
        self.PRIMARY_COMPANIES = ['openai', 'anthropic', 'google', 'deepseek']
    
    def check_for_breaking_news(self, new_posts):
        """Identify if any post is breaking news worthy"""
        breaking_posts = []
        
        for post in new_posts:
            # Check if it mentions a primary company
            has_primary = any(
                company in post.get('companies', {})
                for company in self.PRIMARY_COMPANIES
            )
            
            if not has_primary:
                continue
            
            # Check for breaking keywords in title
            title_lower = post['title'].lower()
            is_breaking = any(
                keyword in title_lower 
                for keyword in self.BREAKING_KEYWORDS
            )
            
            # High relevance score also triggers
            high_relevance = post.get('relevance_score', 0) > 5
            
            if is_breaking or high_relevance:
                # Avoid duplicates
                if post['link'] not in self.cache.get('posted', []):
                    breaking_posts.append(post)
                    self.mark_as_posted(post['link'])
        
        return breaking_posts
    
    def trigger_immediate_build(self, breaking_posts):
        """Trigger GitHub Actions workflow for immediate deploy"""
        for post in breaking_posts:
            print(f"🔥 BREAKING: {post['title']}")
            
            # You could also:
            # 1. Send email alert
            self.send_email_alert(post)
            
            # 2. Post to Twitter/Discord (optional)
            self.post_to_social(post)
        
        # Return special flag for GitHub Actions
        return len(breaking_posts) > 0
    
    def send_email_alert(self, post):
        """Optional: Email yourself for major news"""
        # Configure with your email
        print(f"Would send email for: {post['title']}")
        # Add actual SMTP code if desired
    
    def post_to_social(self, post):
        """Optional: Auto-post to social media"""
        print(f"Would post to social: {post['title']}")
    
    def load_cache(self):
        if self.cache_file.exists():
            self.cache = json.loads(self.cache_file.read_text())
        else:
            self.cache = {'posted': [], 'last_check': None}
    
    def mark_as_posted(self, link):
        self.cache['posted'].append(link)
        self.cache['last_check'] = datetime.now().isoformat()
        self.cache_file.write_text(json.dumps(self.cache, indent=2))
