---
layout: default
title: AI News Dashboard
---

# 🤖 AI News Tracker

{% assign companies = "openai,anthropic,google,deepseek,microsoft,meta" | split: "," %}
{% assign company_names = "OpenAI,Anthropic,Google,DeepSeek,Microsoft,Meta" | split: "," %}

<!-- Today's Featured News -->
## 📌 Today's Top Stories
{% assign today = site.time | date: '%Y-%m-%d' %}
{% assign has_today = false %}

{% for post in site.posts limit:5 %}
  {% assign post_date = post.date | date: '%Y-%m-%d' %}
  {% if post_date == today %}
    {% assign has_today = true %}
    <div class="featured-post">
      <h3><a href="{{ post.link }}" target="_blank">{{ post.title }}</a></h3>
      <small>📰 {{ post.source }} | 
        {% if post.tags %}
          🔥 
          {% for tag in post.tags limit:3 %}
            {% if tag == 'openai' or tag == 'anthropic' or tag == 'google' or tag == 'microsoft' or tag == 'meta' or tag == 'deepseek' %}
              {{ tag | capitalize }}{% unless forloop.last %}, {% endunless %}
            {% endif %}
          {% endfor %}
        {% endif %}
      </small>
      {% if post.content %}
        <p>{{ post.content | strip_html | truncate: 200 }}</p>
      {% endif %}
    </div>
  {% endif %}
{% endfor %}

{% if has_today == false %}
  <p>No new news today. Showing recent highlights:</p>
  {% for post in site.posts limit:3 %}
    <div class="recent-post">
      <h3><a href="{{ post.link }}" target="_blank">{{ post.title }}</a></h3>
      <small>📰 {{ post.source }} | 📅 {{ post.date | date: '%b %d' }} | 
        {% if post.tags %}
          🏢 
          {% for tag in post.tags limit:2 %}
            {% if tag == 'openai' or tag == 'anthropic' or tag == 'google' or tag == 'microsoft' or tag == 'meta' or tag == 'deepseek' %}
              {{ tag | capitalize }}{% unless forloop.last %}, {% endunless %}
            {% endif %}
          {% endfor %}
        {% endif %}
      </small>
    </div>
  {% endfor %}
{% endif %}

<!-- Company-Specific Sections -->
## 🏢 News by Company

<div class="company-grid">
  {% for i in (0..5) %}
    {% assign company = companies[i] %}
    {% assign display_name = company_names[i] %}
    
    <div class="company-section">
      <h3>{{ display_name }}</h3>
      <ul>
        {% assign count = 0 %}
        {% for post in site.posts %}
          {% if post.tags contains company and count < 5 %}
            {% assign count = count | plus: 1 %}
            <li>
              <a href="{{ post.link }}" target="_blank">{{ post.title }}</a>
              <small>({{ post.source }}, {{ post.date | date: '%b %d' }})</small>
            </li>
          {% endif %}
        {% endfor %}
        
        {% if count == 0 %}
          <li><em>No recent news</em></li>
        {% endif %}
      </ul>
    </div>
  {% endfor %}
</div>

<!-- Source Health Dashboard -->
## 📊 Feed Health Monitor

<div class="health-dashboard">
  <table>
    <tr>
      <th>Source</th>
      <th>Status</th>
      <th>Last Fetch</th>
      <th>Articles Today</th>
      <th>Success Rate</th>
    </tr>
    {% if site.data.source_health %}
      {% for source in site.data.source_health %}
      <tr>
        <td>{{ source.name }}</td>
        <td>
          {% if source.status == 'healthy' %}
            ✅
          {% elsif source.status == 'degraded' %}
            ⚠️
          {% else %}
            ❌
          {% endif %}
        </td>
        <td>{{ source.last_fetch | date: '%H:%M' }}</td>
        <td>{{ source.articles_today }}</td>
        <td>{{ source.success_rate }}%</td>
      </tr>
      {% endfor %}
    {% else %}
      <tr>
        <td colspan="5">Loading health data...</td>
      </tr>
    {% endif %}
  </table>
</div>

<!-- Add some CSS to make it look nice -->
<style>
.company-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin: 20px 0;
}
.company-section {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
}
.company-section ul {
  margin: 10px 0 0 0;
  padding-left: 20px;
}
.company-section li {
  margin-bottom: 8px;
}
.featured-post {
  background: #e8f4fe;
  padding: 15px;
  border-left: 4px solid #0366d6;
  margin: 10px 0;
  border-radius: 0 4px 4px 0;
}
.recent-post {
  background: #f9f9f9;
  padding: 12px;
  margin: 8px 0;
  border-radius: 4px;
}
.health-dashboard {
  margin: 20px 0;
  overflow-x: auto;
}
.health-dashboard table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}
.health-dashboard th {
  background: #f0f0f0;
  padding: 10px;
  text-align: left;
  border-bottom: 2px solid #ddd;
}
.health-dashboard td {
  padding: 8px 10px;
  border-bottom: 1px solid #eee;
}
.health-dashboard tr:hover {
  background: #f5f5f5;
}
small {
  color: #666;
  font-size: 0.9em;
}
a {
  color: #0366d6;
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
</style>
