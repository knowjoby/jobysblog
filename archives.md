---
layout: page
title: Archives
permalink: /archives/
---

# Archives

Search and filter *published* posts (the public feed). The internal queue is intentionally not exposed here.

<div style="display:flex; gap:10px; align-items:center; margin: 16px 0; flex-wrap: wrap;">
  <input id="archiveSearch" type="text" placeholder="Search title, source, tags…" style="flex:1 1 280px; padding:10px 12px; border:1px solid #ddd; border-radius:8px;">
  <button id="archiveClear" type="button" style="padding:10px 12px; border:1px solid #ddd; border-radius:8px; background:#fff; cursor:pointer;">Clear</button>
</div>

<div id="archiveActiveFilter" style="display:none; margin: 8px 0; padding: 8px 12px; border-radius: 8px; background: #f6f8fa; border: 1px solid #eee; font-size: 14px;"></div>

<table id="archiveTable">
  <thead>
    <tr>
      <th style="text-align:left;">Date</th>
      <th style="text-align:left;">Title</th>
      <th style="text-align:left;">Source</th>
      <th style="text-align:left;">Tags</th>
      <th style="text-align:right;">Score</th>
    </tr>
  </thead>
  <tbody>
  {%- assign posts = site.posts | where_exp: "post", "post.categories contains 'ai-news'" -%}
  {%- for post in posts -%}
    {%- assign tags = post.tags | join: " " -%}
    {%- assign source = post.source | default: "" -%}
    {%- if post.link -%}
      {%- assign href = post.link -%}
      {%- assign target = "_blank" -%}
      {%- assign rel = "noopener" -%}
    {%- else -%}
      {%- assign href = post.url | relative_url -%}
      {%- assign target = "" -%}
      {%- assign rel = "" -%}
    {%- endif -%}

    <tr class="archiveRow"
        data-title="{{ post.title | escape | replace: '&amp;#8217;', '’' | replace: '&#8217;', '’' | replace: '&amp;rsquo;', '’' | replace: '&rsquo;', '’' | downcase }}"
        data-source="{{ source | downcase }}"
        data-tags="{{ tags | downcase }}"
        data-score="{{ post.score | default: 0 | plus: 0 }}">
      <td style="white-space:nowrap;">{{ post.date | date: "%Y-%m-%d" }}</td>
      <td>
        <a href="{{ href }}"{% if target != "" %} target="{{ target }}"{% endif %}{% if rel != "" %} rel="{{ rel }}"{% endif %}>
          {{ post.title | escape | replace: '&amp;#8217;', '’' | replace: '&#8217;', '’' | replace: '&amp;rsquo;', '’' | replace: '&rsquo;', '’' }}
        </a>
      </td>
      <td style="white-space:nowrap;">{{ source }}</td>
      <td>
        {%- if post.tags and post.tags.size > 0 -%}
          {%- for tag in post.tags -%}
            <button type="button" class="archiveTag" data-tag="{{ tag | downcase }}" style="margin:2px 4px 2px 0; padding:2px 8px; border-radius:999px; border:1px solid #eee; background:#f8f9fa; cursor:pointer; font-size:12px;">
              {{ tag }}
            </button>
          {%- endfor -%}
        {%- endif -%}
      </td>
      <td style="text-align:right; font-variant-numeric: tabular-nums;">{{ post.score | default: 0 }}</td>
    </tr>
  {%- endfor -%}
  </tbody>
</table>

<p id="archiveCount" style="margin-top: 12px; color: #666;"></p>

<script>
  (function() {
    var searchEl = document.getElementById('archiveSearch');
    var clearEl = document.getElementById('archiveClear');
    var activeEl = document.getElementById('archiveActiveFilter');
    var rows = Array.from(document.querySelectorAll('.archiveRow'));

    var activeTag = null;

    function applyFilter() {
      var q = (searchEl.value || '').trim().toLowerCase();
      var visible = 0;

      rows.forEach(function(row) {
        var hay = [row.dataset.title, row.dataset.source, row.dataset.tags].join(' ');
        var ok = true;
        if (q && hay.indexOf(q) === -1) ok = false;
        if (activeTag && row.dataset.tags.indexOf(activeTag) === -1) ok = false;

        row.style.display = ok ? '' : 'none';
        if (ok) visible++;
      });

      var msg = [];
      if (activeTag) msg.push('tag: ' + activeTag);
      if (q) msg.push('search: ' + q);
      if (msg.length > 0) {
        activeEl.textContent = 'Filtering by ' + msg.join(' • ');
        activeEl.style.display = 'block';
      } else {
        activeEl.style.display = 'none';
      }

      document.getElementById('archiveCount').textContent = visible + ' posts shown';
    }

    document.querySelectorAll('.archiveTag').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var t = btn.dataset.tag;
        activeTag = (activeTag === t) ? null : t;
        applyFilter();
      });
    });

    searchEl.addEventListener('input', applyFilter);
    clearEl.addEventListener('click', function() {
      activeTag = null;
      searchEl.value = '';
      applyFilter();
    });

    applyFilter();
  })();
</script>
