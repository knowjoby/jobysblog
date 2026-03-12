---
layout: page
title: About
---

This is an automated AI news feed — a personal linklog tracking what's happening across the AI industry.

**What it covers**

Releases, product launches, controversies, safety incidents, funding rounds, and anything notable from companies like Anthropic, OpenAI, Google DeepMind, Microsoft, Meta, xAI, and others building AI models.

**How it works**

An automation runs continuously (every ~30 minutes) and:

1. Fetches fresh AI news (DDG News when available; RSS fallback when DDG is blocked on runners)
2. Filters for AI relevance (company + topic keyword rules)
3. Scores stories (0–100) based on recency + importance
4. Publishes the top items as posts on this site (usually outbound links)
5. Commits to `main`, which triggers an automatic GitHub Pages deploy

No paywalls bypassed, no scraping tricks — just public headlines + links, scored and organized.

**Sources**

RSS fallback sources:

{% assign sources = site.data.rss_sources | default: "" %}
{% if sources and sources.size > 0 %}
<ul>
{% for s in sources %}
  <li><a href="{{ s.url }}" target="_blank" rel="noopener">{{ s.name }}</a></li>
{% endfor %}
</ul>
{% else %}
(No RSS sources file found.)
{% endif %}

**What the dots mean**

- 🟢 Score ≥ 75 — high signal, worth reading
- 🟠 Score ≥ 50 — decent story
- ⚫ Below 50 — minor or background noise

**Tags**

Each post is auto-tagged by company (`anthropic`, `openai`, `google` …) and topic (`release`, `controversy`, `safety`, `rumor` …) so you can skim by what matters to you.

**Logs**

The [Status]({{ "/logs/" | relative_url }}) page shows the latest run + recent run history.
