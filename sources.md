---
layout: page
title: Sources
permalink: /sources/
---

# Sources

This page lists the RSS sources used by the automation (as the reliable fallback when DDG News is blocked on runners).

{% assign sources = site.data.rss_sources | default: "" %}
{% if sources and sources.size > 0 %}
<ul>
{% for s in sources %}
  <li><a href="{{ s.url }}" target="_blank" rel="noopener">{{ s.name }}</a></li>
{% endfor %}
</ul>
{% else %}
No sources file found.
{% endif %}

