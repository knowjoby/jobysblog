---
layout: page
title: Logs
permalink: /logs/
---

<style>
  .log-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    font-family: 'Inter', sans-serif;
    margin-top: 1.5rem;
  }
  .log-table th {
    background: #f5f5f5;
    border: 1px solid #ddd;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    color: #333;
    white-space: nowrap;
  }
  .log-table td {
    border: 1px solid #ddd;
    padding: 10px 14px;
    vertical-align: top;
    color: #444;
  }
  .log-table tr:hover td {
    background: #fafafa;
  }
  .badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
  }
  .badge-schedule  { background: #e8f5e9; color: #2e7d32; }
  .badge-manual    { background: #e3f2fd; color: #1565c0; }
  .badge-local     { background: #f3e5f5; color: #6a1b9a; }
  .score-pill {
    display: inline-block;
    padding: 1px 7px;
    border-radius: 10px;
    font-size: 11px;
    font-weight: 600;
    background: #fff3e0;
    color: #e65100;
    margin-right: 4px;
  }
  .post-link {
    display: block;
    margin-bottom: 4px;
    color: #555;
    text-decoration: none;
    font-size: 13px;
  }
  .post-link:hover { color: #000; text-decoration: underline; }
  .tag {
    display: inline-block;
    font-size: 11px;
    background: #eee;
    color: #666;
    padding: 1px 6px;
    border-radius: 4px;
    margin: 1px 2px 0 0;
  }
  .meta-row td {
    font-size: 13px;
    color: #888;
  }
  .empty-state {
    text-align: center;
    padding: 3rem;
    color: #aaa;
    font-style: italic;
  }
  .feed-ok   { color: #4caf50; font-weight: 600; }
  .feed-fail { color: #e53935; font-weight: 600; }
  .feed-fail-name {
    display: inline-block;
    font-size: 11px;
    background: #fdecea;
    color: #c62828;
    padding: 1px 6px;
    border-radius: 4px;
    margin: 2px 2px 0 0;
  }
</style>

{% if site.data.run_log and site.data.run_log.size > 0 %}

{% assign runs = site.data.run_log | reverse %}

<p style="color:#888; font-size:13px; margin-bottom:0;">
  {{ site.data.run_log.size }} run(s) recorded &nbsp;·&nbsp;
  {% assign total_posts = 0 %}
  {% for run in site.data.run_log %}{% assign total_posts = total_posts | plus: run.posts_created %}{% endfor %}
  {{ total_posts }} post(s) published total
</p>

<table class="log-table">
  <thead>
    <tr>
      <th>#</th>
      <th>Date &amp; Time (IST)</th>
      <th>Triggered By</th>
      <th>Candidates</th>
      <th>Posts Created</th>
      <th>Queued</th>
      <th>Sources</th>
      <th>Articles</th>
    </tr>
  </thead>
  <tbody>
    {% assign run_count = site.data.run_log.size %}
    {% for run in runs %}
      {% assign run_num = run_count | minus: forloop.index0 %}

      {% if run.triggered_by contains "Scheduled" %}
        {% assign badge_class = "badge-schedule" %}
      {% elsif run.triggered_by contains "GitHub" %}
        {% assign badge_class = "badge-manual" %}
      {% else %}
        {% assign badge_class = "badge-local" %}
      {% endif %}

      <tr>
        <td style="color:#bbb; font-size:12px;">{{ run_num }}</td>
        <td style="white-space:nowrap; font-variant-numeric: tabular-nums;">{{ run.ran_at }}</td>
        <td><span class="badge {{ badge_class }}">{{ run.triggered_by }}</span></td>
        <td style="text-align:center;">{{ run.candidates_found }}</td>
        <td style="text-align:center; font-weight:600;">
          {% if run.posts_created == 0 %}
            <span style="color:#bbb;">0</span>
          {% else %}
            {{ run.posts_created }}
          {% endif %}
        </td>
        <td style="text-align:center; color:#888;">{{ run.queued }}</td>
        <td>
          {% if run.feeds %}
            {% assign ok_count = 0 %}
            {% assign fail_count = 0 %}
            {% for feed in run.feeds %}
              {% if feed[1].ok %}
                {% assign ok_count = ok_count | plus: 1 %}
              {% else %}
                {% assign fail_count = fail_count | plus: 1 %}
              {% endif %}
            {% endfor %}
            <span class="feed-ok">✓{{ ok_count }}</span>
            {% if fail_count > 0 %}
              <span class="feed-fail"> ✗{{ fail_count }}</span>
              <div style="margin-top:4px;">
                {% for feed in run.feeds %}
                  {% unless feed[1].ok %}
                    <span class="feed-fail-name">{{ feed[0] }}</span>
                  {% endunless %}
                {% endfor %}
              </div>
            {% endif %}
          {% else %}
            <span style="color:#ddd; font-size:12px;">—</span>
          {% endif %}
        </td>
        <td>
          {% if run.posts and run.posts.size > 0 %}
            {% for post in run.posts %}
              <div style="margin-bottom:6px;">
                <span class="score-pill">{{ post.score }}</span>
                <a class="post-link" href="{{ site.baseurl }}/{{ post.file | remove: '_posts/' | remove: '.md' | replace: '-', '/' | prepend: '' }}">{{ post.title }}</a>
                {% for tag in post.tags %}<span class="tag">{{ tag }}</span>{% endfor %}
              </div>
            {% endfor %}
          {% else %}
            <span style="color:#ccc; font-size:12px;">— no posts —</span>
          {% endif %}
        </td>
      </tr>
    {% endfor %}
  </tbody>
</table>

{% else %}
<div class="empty-state">No runs recorded yet.</div>
{% endif %}
