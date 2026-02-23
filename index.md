---
layout: home
{% assign companies = "openai,anthropic,google,deepseek" | split: "," %}
{% for company in companies %}
  <h3>{{ company | capitalize }} News</h3>
  <ul>
  {% for post in site.posts %}
    {% if post.companies contains company %}
      <li>
        <a href="{{ post.link }}">{{ post.title }}</a>
        <small>(via {{ post.source }})</small>
      </li>
    {% endif %}
  {% endfor %}
  </ul>
{% endfor %}
---
