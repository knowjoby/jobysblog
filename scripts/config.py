#!/usr/bin/env python3
"""
Shared configuration for AI news aggregator.
Single source of truth for keywords, RSS feeds, and utility functions.
"""

import re
from typing import List, Dict, Any, Set, Union

# =============================================================================
# COMPANY KEYWORDS (Tier 1 - Major AI Companies)
# =============================================================================
COMPANY_KEYWORDS: Dict[str, List[str]] = {
    # Tier 1 (Established leaders)
    "openai": [
        "openai", "chatgpt", "gpt-4", "gpt4", "gpt-4o", "gpt4o", "o1", "o3",
        "sora", "dall-e", "dalle", "whisper", "sam altman", "open ai"
    ],
    "anthropic": [
        "anthropic", "claude", "claude 3", "claude 3.5", "claude 3.7", "claude 4",
        "constitutional ai", "dario amodei", "claude ai"
    ],
    "google": [
        "google ai", "google deepmind", "deepmind", "gemini", "bard", "palm 2",
        "palm2", "imagen", "veo", "alphafold", "demis hassabis", "geminiai",
        "google gemini", "vertex ai"
    ],
    "microsoft": [
        "microsoft ai", "copilot", "azure ai", "bing ai", "microsoft research",
        "phi-3", "phi3", "phi-4", "phi4", "satya nadella", "msft ai"
    ],
    "meta": [
        r"\bmeta\b", "meta ai", "llama", "llama 2", "llama 3", "llama 3.1",
        "llama 3.2", "llama 3.3", "llama 4", "yann lecun", "metamate",
        "meta llama", "meta generative ai"
    ],
    "xai": [
        "xai", "x ai", "grok", "elon musk ai", "elon ai", "x.ai"
    ],
    "amazon": [
        "amazon ai", "aws ai", "alexa ai", "bedrock", "sagemaker", "aws bedrock",
        "amazon q", "amazon titan", "amazon agi"
    ],
    "apple": [
        "apple intelligence", "apple ai", "apple machine learning", "siri ai",
        "mlx", "apple ml", "ferret ui", "apple ferro", "john giannandrea"
    ],
    "nvidia": [
        "nvidia", "jensen huang", "h100", "h200", "a100", "b200", "blackwell",
        "rubin", "dgx", "cuda", "tensorrt", "nvidia ai", "gpu", "ai chip",
        "nvidia inference"
    ],
    
    # Tier 2 (Emerging/notable)
    "deepseek": [
        "deepseek", "deep seek", "deepseek v2", "deepseek v3", "deepseek r1"
    ],
    "mistral": [
        "mistral", "mistral ai", "mistral 7b", "mixtral", "mistral large",
        "le chat"
    ],
    "cohere": [
        "cohere", "command r", "rerank", "aidan gomez"
    ],
    "perplexity": [
        "perplexity", "perplexity ai", "pplx"
    ],
    "midjourney": [
        "midjourney", "mj ai"
    ],
    "stability": [
        "stability ai", "stable diffusion", "sd3", "stable video"
    ],
    "figure": [
        "figure ai", "figure 01", "figure 02", "figure robotics"
    ],
    "adept": [
        "adept ai", "act-1"
    ],
    "huggingface": [
        "huggingface", "hugging face", "transformers"
    ]
}

# =============================================================================
# TOPIC KEYWORDS (Thematic categories)
# =============================================================================
TOPIC_KEYWORDS: Dict[str, List[str]] = {
    "agentic": [
        r"\bagent\b", r"\bagentic\b", "ai agent", "autonomous agent",
        "agent framework", "agent orchestration", "agentic ai"
    ],
    "reasoning": [
        r"\breasoning\b", "chain of thought", "system 2", "deliberation",
        "logical reasoning", "multistep reasoning"
    ],
    "regulation": [
        "regulation", "compliance", "ai act", "executive order", "governance",
        "oversight", "safety standards", "red team"
    ],
    "robotics": [
        "robot", "robotics", "humanoid", "manipulation", "embodied",
        "ros", "robotic learning"
    ],
    "coding": [
        "coding", "programming", "code generation", "software engineer",
        "developer tools", "copilot", "code assistant"
    ],
    "multimodal": [
        "multimodal", "vision language", "image generation", "video generation",
        "text to image", "text to video"
    ],
    "open_source": [
        "open source", "opensource", "weights release", "model release",
        "source available"
    ],
    "china": [
        "china ai", "chinese ai", "beijing ai", "shenzhen ai"
    ]
}

# =============================================================================
# RSS FEED SOURCES
# =============================================================================
RSS_FEEDS: List[Dict[str, Any]] = [
    # Primary sources (high authority)
    {"url": "https://techcrunch.com/category/artificial-intelligence/feed/", "name": "TechCrunch AI", "primary": True},
    {"url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml", "name": "The Verge AI", "primary": True},
    {"url": "https://venturebeat.com/category/ai/feed/", "name": "VentureBeat AI", "primary": True},
    
    # Company blogs (higher authority for specific news)
    {"url": "https://openai.com/blog/rss/", "name": "OpenAI Blog", "primary": False},
    {"url": "https://www.anthropic.com/news/rss.xml", "name": "Anthropic News", "primary": False},
    {"url": "https://deepmind.google/blog/rss.xml", "name": "DeepMind Blog", "primary": False},
    {"url": "https://ai.meta.com/blog/rss.xml", "name": "Meta AI Blog", "primary": False},
    {"url": "https://blogs.microsoft.com/ai/feed/", "name": "Microsoft AI Blog", "primary": False},
    
    # Research & technical
    {"url": "https://arxiv.org/rss/cs.ai", "name": "arXiv AI", "primary": False},
    {"url": "https://huggingface.co/blog/feed.xml", "name": "Hugging Face Blog", "primary": False},
    {"url": "https://lmsys.org/blog/index.xml", "name": "LMSYS Org", "primary": False},
    
    # News aggregators
    {"url": "https://www.artificialintelligence-news.com/feed/", "name": "AI News", "primary": False},
    {"url": "https://www.ainewsletter.com/newsletter.rss", "name": "AI Newsletter", "primary": False},
    {"url": "https://aibusiness.com/feed.rss", "name": "AI Business", "primary": False},
]

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def match_keywords(text: str, keyword_list: List[str]) -> bool:
    """
    Match text against a list of keywords using word-boundary regex.
    
    Args:
        text: The text to search in (title + description/summary)
        keyword_list: List of keywords or regex patterns
        
    Returns:
        True if any keyword matches, False otherwise
    """
    if not text or not keyword_list:
        return False
        
    text_lower = text.lower()
    
    for keyword in keyword_list:
        # If keyword is already a regex pattern (starts with r'\b' etc), use as is
        if keyword.startswith(r'\b') or '\\b' in keyword:
            pattern = keyword
        else:
            # Escape regex special characters and add word boundaries
            escaped = re.escape(keyword)
            pattern = r'\b' + escaped + r'\b'
        
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    
    return False


def detect_companies(text: str) -> List[str]:
    """
    Detect which companies are mentioned in the text.
    
    Args:
        text: Combined text to search in
        
    Returns:
        List of company keys that matched
    """
    companies_found = []
    
    for company, keywords in COMPANY_KEYWORDS.items():
        if match_keywords(text, keywords):
            companies_found.append(company)
    
    return companies_found


def detect_topics(text: str) -> List[str]:
    """
    Detect which topics are mentioned in the text.
    
    Args:
        text: Combined text to search in
        
    Returns:
        List of topic keys that matched
    """
    topics_found = []
    
    for topic, keywords in TOPIC_KEYWORDS.items():
        if match_keywords(text, keywords):
            topics_found.append(topic)
    
    return topics_found


def get_primary_feeds() -> List[Dict[str, Any]]:
    """Return only primary RSS feeds."""
    return [feed for feed in RSS_FEEDS if feed.get("primary", False)]


def get_all_feeds() -> List[Dict[str, Any]]:
    """Return all RSS feeds."""
    return RSS_FEEDS


def get_company_tier(company: str) -> int:
    """
    Determine tier of a company (1 for major, 2 for emerging).
    
    Args:
        company: Company key
        
    Returns:
        1 for tier 1, 2 for tier 2
    """
    tier1_companies = [
        "openai", "anthropic", "google", "microsoft", "meta", "xai",
        "amazon", "apple", "nvidia"
    ]
    
    return 1 if company in tier1_companies else 2