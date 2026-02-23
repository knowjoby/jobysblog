---
layout: default
title: Changelog
permalink: /changelog/
---

# 📋 Changelog & Development Log

Track the evolution of this AI news aggregator, including features added, improvements made, and the AI tools that helped build it.

## 🚀 Latest Updates

<div class="timeline">

  <div class="timeline-item current">
    <div class="timeline-badge">✨</div>
    <div class="timeline-content">
      <h3>Archives Page Added</h3>
      <div class="date">February 23, 2026</div>
      <p>Added comprehensive archives page with:</p>
      <ul>
        <li>Company filtering (OpenAI, Anthropic, Google, etc.)</li>
        <li>Search functionality across titles and sources</li>
        <li>Sortable columns for date, title, source, and score</li>
        <li>Color-coded score badges (green/yellow/red)</li>
        <li>Pagination (20 articles per page)</li>
      </ul>
      <div class="ai-tools">
        <span class="tool-tag">🤖 Claude 3.5 Sonnet</span>
        <span class="tool-tag">⚡ GitHub Copilot</span>
      </div>
    </div>
  </div>

  <div class="timeline-item">
    <div class="timeline-badge">📊</div>
    <div class="timeline-content">
      <h3>Enhanced Queue Management</h3>
      <div class="date">February 23, 2026</div>
      <p>Improved article queue system:</p>
      <ul>
        <li>Added queue_status.py for monitoring pending articles</li>
        <li>Implemented 14-day automatic cleanup of old items</li>
        <li>Score-based prioritization (93 down to 67)</li>
        <li>Per-company posting limits (max 2/day per company)</li>
      </ul>
      <div class="ai-tools">
        <span class="tool-tag">🤖 Claude 3.5 Sonnet</span>
      </div>
    </div>
  </div>

  <div class="timeline-item">
    <div class="timeline-badge">🔍</div>
    <div class="timeline-content">
      <h3>Advanced Company Detection</h3>
      <div class="date">February 23, 2026</div>
      <p>Integrated ai_news_filter.py for smarter company identification:</p>
      <ul>
        <li>Detailed keyword matching for 10+ AI companies</li>
        <li>Relevance scoring for mentions</li>
        <li>Primary company detection for each article</li>
      </ul>
      <div class="ai-tools">
        <span class="tool-tag">🤖 Claude 3.5 Sonnet</span>
        <span class="tool-tag">🐍 Python</span>
      </div>
    </div>
  </div>

  <div class="timeline-item">
    <div class="timeline-badge">🚨</div>
    <div class="timeline-content">
      <h3>Breaking News Monitor</h3>
      <div class="date">February 23, 2026</div>
      <p>Added breaking_news_monitor.py to detect major announcements:</p>
      <ul>
        <li>Keyword detection for "GPT-5", "Claude 4", "Gemini Ultra"</li>
        <li>High-relevance score triggers (85+)</li>
        <li>Immediate build triggers for major news</li>
      </ul>
      <div class="ai-tools">
        <span class="tool-tag">🤖 Claude 3.5 Sonnet</span>
      </div>
    </div>
  </div>

  <div class="timeline-item">
    <div class="timeline-badge">📈</div>
    <div class="timeline-content">
      <h3>Feed Health Monitoring</h3>
      <div class="date">February 23, 2026</div>
      <p>Implemented source_health.yml tracking:</p>
      <ul>
        <li>Per-source success rate monitoring</li>
        <li>Last fetch timestamps</li>
        <li>Article count tracking</li>
        <li>Error logging for failed feeds</li>
      </ul>
      <div class="ai-tools">
        <span class="tool-tag">🤖 Claude 3.5 Sonnet</span>
      </div>
    </div>
  </div>

  <div class="timeline-item">
    <div class="timeline-badge">🎯</div>
    <div class="timeline-content">
      <h3>Scoring Algorithm Refinement</h3>
      <div class="date">February 22, 2026</div>
      <p>Enhanced article scoring in generate_news.py:</p>
      <ul>
        <li>Recency scoring (0-25 points)</li>
        <li>Company tier system (Tier 1: OpenAI, Anthropic, Google, Microsoft)</li>
        <li>Topic importance weights (safety: 30, controversy: 28, release: 22)</li>
        <li>Uniqueness detection across sources</li>
      </ul>
      <div class="ai-tools">
        <span class="tool-tag">🤖 Claude 3.5 Sonnet</span>
        <span class="tool-tag">📊 Data analysis</span>
      </div>
    </div>
  </div>

  <div class="timeline-item">
    <div class="timeline-badge">🤖</div>
    <div class="timeline-content">
      <h3>Initial AI News Pipeline</h3>
      <div class="date">February 22, 2026</div>
      <p>Core infrastructure established:</p>
      <ul>
        <li>13 RSS feeds from tech media, company blogs, and newsletters</li>
        <li>Jekyll blog with minima theme</li>
        <li>GitHub Actions automation</li>
        <li>Daily posting limit: 5 articles</li>
        <li>Queue system for pending articles</li>
      </ul>
      <div class="ai-tools">
        <span class="tool-tag">🤖 Claude 3.5 Sonnet</span>
        <span class="tool-tag">🐍 Python</span>
        <span class="tool-tag">🔧 Jekyll</span>
        <span class="tool-tag">⚡ GitHub Actions</span>
      </div>
    </div>
  </div>

</div>

## 🛠️ AI Tools & Technologies Used

<div class="tools-grid">
  <div class="tool-card">
    <div class="tool-icon">🤖</div>
    <h3>Claude 3.5 Sonnet</h3>
    <p>Primary AI assistant for code generation, architecture design, and troubleshooting throughout development.</p>
  </div>
  
  <div class="tool-card">
    <div class="tool-icon">⚡</div>
    <h3>GitHub Copilot</h3>
    <p>Used for code completion and suggesting improvements in Python scripts and Jekyll templates.</p>
  </div>
  
  <div class="tool-card">
    <div class="tool-icon">🐍</div>
    <h3>Python</h3>
    <p>Core language for RSS fetching, article scoring, and queue management.</p>
  </div>
  
  <div class="tool-card">
    <div class="tool-icon">🔧</div>
    <h3>Jekyll & Liquid</h3>
    <p>Static site generation with dynamic content rendering using Liquid templates.</p>
  </div>
  
  <div class="tool-card">
    <div class="tool-icon">⚙️</div>
    <h3>GitHub Actions</h3>
    <p>Automated daily builds and deployments triggered by schedule or manual dispatch.</p>
  </div>
  
  <div class="tool-card">
    <div class="tool-icon">📰</div>
    <h3>Feedparser</h3>
    <p>Python library for parsing RSS/Atom feeds from 13+ sources.</p>
  </div>
</div>

## 📊 Development Statistics

<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-number">13+</div>
    <div class="stat-label">RSS Feeds</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">8</div>
    <div class="stat-label">Python Scripts</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">127</div>
    <div class="stat-label">Articles/Week</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">5</div>
    <div class="stat-label">Daily Posts</div>
  </div>
</div>

## 🔮 Planned Features

- [ ] Sentiment analysis for article tone detection
- [ ] Weekly summary email newsletter
- [ ] Trending topics visualization
- [ ] Source quality scoring
- [ ] Mobile app notifications for breaking news

---

*Last updated: February 23, 2026*

<style>
.timeline {
  position: relative;
  max-width: 800px;
  margin: 40px auto;
  padding-left: 50px;
}
.timeline::before {
  content: '';
  position: absolute;
  left: 20px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e1e4e8;
}
.timeline-item {
  position: relative;
  margin-bottom: 40px;
}
.timeline-badge {
  position: absolute;
  left: -50px;
  width: 40px;
  height: 40px;
  background: white;
  border: 2px solid #0366d6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  z-index: 1;
}
.timeline-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.timeline-content h3 {
  margin: 0 0 5px 0;
  color: #24292e;
}
.timeline-content .date {
  color: #586069;
  font-size: 14px;
  margin-bottom: 10px;
}
.timeline-content ul {
  margin: 10px 0;
  padding-left: 20px;
}
.timeline-content li {
  margin: 5px 0;
  color: #444;
}
.ai-tools {
  margin-top: 15px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.tool-tag {
  background: #f1f8ff;
  color: #0366d6;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  border: 1px solid #c8e1ff;
}
.timeline-item.current .timeline-content {
  border-left: 4px solid #2cbe4e;
}
.timeline-item.current .timeline-badge {
  border-color: #2cbe4e;
}
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin: 30px 0;
}
.tool-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  text-align: center;
}
.tool-icon {
  font-size: 40px;
  margin-bottom: 10px;
}
.tool-card h3 {
  margin: 10px 0;
  color: #24292e;
}
.tool-card p {
  color: #586069;
  font-size: 14px;
  line-height: 1.5;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  margin: 30px 0;
}
.stat-card {
  background: #f6f8fa;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}
.stat-number {
  font-size: 36px;
  font-weight: bold;
  color: #0366d6;
}
.stat-label {
  color: #586069;
  margin-top: 5px;
}
</style>
