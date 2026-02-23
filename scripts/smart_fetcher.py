# scripts/smart_fetcher.py

import time
from datetime import datetime, timedelta
import json
from pathlib import Path

class SmartNewsFetcher:
    def __init__(self):
        self.last_run_file = Path('data/last_fetch_times.json')
        self.last_runs = self.load_last_runs()
        self.schedules = {
            'high': {'interval': 30, 'sources': [...]},
            'medium': {'interval': 120, 'sources': [...]},
            'low': {'interval': 360, 'sources': [...]},
        }
    
    def should_fetch_source(self, source_name, source_type):
        """Check if enough time has passed since last fetch"""
        last_fetch = self.last_runs.get(source_name)
        if not last_fetch:
            return True
        
        interval = self.schedules[source_type]['interval']
        next_fetch = datetime.fromisoformat(last_fetch) + timedelta(minutes=interval)
        
        return datetime.now() >= next_fetch
    
    def fetch_due_sources(self):
        """Only fetch sources that are due for update"""
        for source_type, config in self.schedules.items():
            for source in config['sources']:
                if self.should_fetch_source(source['name'], source_type):
                    self.fetch_source(source)
                    self.update_last_run(source['name'])
        
        self.save_last_runs()
    
    def fetch_source(self, source):
        """Your existing fetch logic here"""
        pass
    
    def load_last_runs(self):
        if self.last_run_file.exists():
            return json.loads(self.last_run_file.read_text())
        return {}
    
    def save_last_runs(self):
        self.last_run_file.write_text(json.dumps(self.last_runs, indent=2))
