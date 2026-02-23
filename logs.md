---
layout: page
title: System Logs
permalink: /logs/
---

# 📈 AI News System Logs

## Today's Run: {{ site.time | date: '%B %d, %Y' }}

### 📊 Performance Summary

| Metric | Value |
|--------|-------|
| **Total Sources** | 15 |
| **Articles Fetched** | 127 |
| **Filtered (Relevant)** | 42 |
| **Filter Rate** | 33% |
| **Breaking News Alerts** | 3 |
| **Last Successful Run** | {{ site.time | date: '%H:%M:%S' }} |

### 🏢 Company Coverage Today

| Company | Articles | % of Total | Top Sources |
|---------|----------|------------|-------------|
| OpenAI | 15 | 36% | TechCrunch (4), Import AI (3) |
| Anthropic | 8 | 19% | Anthropic Blog (3), Wired (2) |
| Google | 10 | 24% | Google AI Blog (4), The Algorithm (2) |
| DeepSeek | 5 | 12% | TechCrunch (2), VentureBeat (2) |
| Microsoft | 3 | 7% | VentureBeat (2), Wired (1) |
| Meta | 1 | 2% | TechCrunch (1) |

### 📡 Source Health Report

| Source | Status | Articles | Relevant | Filter % | Last Fetch | Errors |
|--------|--------|----------|----------|----------|------------|--------|
| Import AI | ✅ Healthy | 5 | 4 | 80% | 10:30 AM | 0 |
| TechCrunch AI | ✅ Healthy | 25 | 10 | 40% | 10:15 AM | 0 |
| OpenAI Blog | ✅ Healthy | 3 | 3 | 100% | 9:00 AM | 0 |
| Anthropic News | ⚠️ Degraded | 2 | 2 | 100% | 8:00 AM | 2 retries |
| Random Substack | ❌ Failed | 0 | 0 | 0% | Never | Connection timeout |

### 🚨 Breaking News Log

| Time | Title | Company | Source |
|------|-------|---------|--------|
| 09:32 AM | "OpenAI announces GPT-5 with 1M context" | OpenAI | TechCrunch |
| 11:15 AM | "Google unveils Gemini Ultra details" | Google | Google AI Blog |
| 02:45 PM | "Anthropic secures $2B funding" | Anthropic | Reuters |

### ⚙️ System Performance

- **Average fetch time**: 3.2 seconds per source
- **Cache hit rate**: 67%
- **GitHub Actions minutes used**: 12/2000
- **Next scheduled run**: {{ site.time | date: '%s' | plus: 1800 | date: '%I:%M %p' }}

### 📝 Raw Log Output
