# scripts/smart_scheduler.py

REFRESH_SCHEDULES = {
    'high_frequency': {
        'sources': ['TechCrunch AI', 'VentureBeat AI', 'Wired AI'],
        'interval': 30,  # minutes
        'reason': 'Professional tech news sites publish multiple times daily'
    },
    'medium_frequency': {
        'sources': ['OpenAI Blog', 'Google AI Blog', 'Anthropic News'],
        'interval': 120,  # 2 hours
        'reason': 'Official company blogs update a few times per week'
    },
    'low_frequency': {
        'sources': ['Import AI', 'The Algorithm', 'AI Snake Oil'],
        'interval': 360,  # 6 hours
        'reason': 'Newsletters/analysis pieces publish 1-3x weekly'
    },
    'static': {
        'sources': ['Academic papers', 'arXiv feeds'],
        'interval': 1440,  # 24 hours
        'reason': 'New papers appear daily, not minute-by-minute'
    }
}
