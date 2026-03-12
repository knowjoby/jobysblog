---
layout: page
title: Now
permalink: /now/
---

# Now

Fast daily briefing: what’s new since your last visit + the highest-signal items from the last 24 hours.

<div id="nowBanner" style="display:none; margin: 12px 0 18px; padding: 10px 12px; border-radius: 10px; border: 1px solid #e8eefc; background: rgba(0,87,255,0.05); color: #0041cc; font-size: 14px;"></div>

## Top 5 (last 24h)

{%- assign now_ts = site.time | date: "%s" | plus: 0 -%}
{%- assign day_seconds = 86400 -%}
{%- assign fresh = "" | split: "" -%}

{%- assign all_ai = site.posts | where_exp: "post", "post.categories contains 'ai-news'" -%}
{%- for post in all_ai -%}
  {%- assign post_ts = post.date | date: "%s" | plus: 0 -%}
  {%- assign age = now_ts | minus: post_ts -%}
  {%- if age >= 0 and age < day_seconds -%}
    {%- assign fresh = fresh | push: post -%}
  {%- endif -%}
{%- endfor -%}

{%- comment -%}
Liquid can't reliably sort by arbitrary keys across all Jekyll setups; we keep this simple:
take the first items (site.posts is reverse-chronological) and show score badges.
{%- endcomment -%}

{%- if fresh.size == 0 -%}
No posts in the last 24 hours.
{%- else -%}
<ol style="padding-left: 18px;">
{%- for post in fresh limit: 5 -%}
  {%- if post.link -%}
    {%- assign href = post.link -%}
    {%- assign target = "_blank" -%}
    {%- assign rel = "noopener" -%}
    {%- assign arrow = "↗" -%}
  {%- else -%}
    {%- assign href = post.url | relative_url -%}
    {%- assign target = "" -%}
    {%- assign rel = "" -%}
    {%- assign arrow = "→" -%}
  {%- endif -%}

  <li class="nowItem" data-pubdate="{{ post.date | date: '%s' }}" style="margin: 10px 0;">
    <a href="{{ href }}"{% if target != "" %} target="{{ target }}"{% endif %}{% if rel != "" %} rel="{{ rel }}"{% endif %} style="text-decoration:none;">
      {{ post.title | escape }}
    </a>
    <span style="color:#888; font-size:12px;">{{ arrow }} · {{ post.date | date: "%b %-d, %H:%M" }} · {{ post.source | default: "post" }}</span>
    {%- if post.score -%}
      <span style="margin-left:8px; font-size:12px; padding:2px 8px; border-radius:999px; border:1px solid #eee; background:#f8f9fa;">score {{ post.score }}</span>
    {%- endif -%}
  </li>
{%- endfor -%}
</ol>
{%- endif -%}

## Recent (new since last visit highlighted)

<ul style="list-style:none; padding-left:0; margin-left:0;">
{%- for post in all_ai limit: 20 -%}
  {%- if post.link -%}
    {%- assign href = post.link -%}
    {%- assign target = "_blank" -%}
    {%- assign rel = "noopener" -%}
    {%- assign arrow = "↗" -%}
  {%- else -%}
    {%- assign href = post.url | relative_url -%}
    {%- assign target = "" -%}
    {%- assign rel = "" -%}
    {%- assign arrow = "→" -%}
  {%- endif -%}

  {%- assign tags = post.tags | join: " " -%}
  <li class="nowItem"
      data-pubdate="{{ post.date | date: '%s' }}"
      data-tags="{{ tags }}"
      style="padding: 8px 10px; border: 1px solid #f0f0f0; border-radius: 10px; margin: 8px 0;">
    <div style="display:flex; gap:10px; align-items:baseline; flex-wrap:wrap;">
      <a href="{{ href }}"{% if target != "" %} target="{{ target }}"{% endif %}{% if rel != "" %} rel="{{ rel }}"{% endif %} style="flex: 1 1 auto;">
        {{ post.title | escape }}
      </a>
      {%- if post.score -%}
        <span style="font-size:12px; padding:2px 8px; border-radius:999px; border:1px solid #eee; background:#f8f9fa; white-space:nowrap;">{{ post.score }}</span>
      {%- endif -%}
      <span style="color:#888; font-size:12px; white-space:nowrap;">{{ arrow }}</span>
    </div>
    <div style="color:#888; font-size:12px; margin-top:4px;">
      {{ post.date | date: "%Y-%m-%d" }} · {{ post.source | default: "post" }}
      {%- if post.tags and post.tags.size > 0 -%}
        · {{ post.tags | join: ", " }}
      {%- endif -%}
    </div>
  </li>
{%- endfor -%}
</ul>

<script>
  (function() {
    var lastVisit = parseInt(localStorage.getItem('ai_now_last_visit') || '0', 10);
    var items = Array.from(document.querySelectorAll('.nowItem[data-pubdate]'));
    var newCount = 0;

    if (lastVisit > 0) {
      items.forEach(function(el) {
        var pubMs = parseInt(el.dataset.pubdate, 10) * 1000;
        if (pubMs > lastVisit) {
          el.style.borderColor = 'rgba(0,87,255,0.35)';
          el.style.background = 'rgba(0,87,255,0.03)';
          newCount++;
        }
      });
    }

    var banner = document.getElementById('nowBanner');
    if (newCount > 0) {
      banner.textContent = newCount + ' new since your last visit';
      banner.style.display = 'block';
    }

    setTimeout(function() {
      localStorage.setItem('ai_now_last_visit', Date.now());
    }, 1500);
  })();
</script>

