---
layout: page
title: Archives
permalink: /archives/
---

# Archives

Two views:

- **Published:** what’s already on the blog
- **Queue:** scored candidates not yet published (deduped)

<div style="display:flex; gap:10px; align-items:center; margin: 16px 0; flex-wrap: wrap;">
  <input id="archiveSearch" type="text" placeholder="Search title, source, tags…" style="flex:1 1 280px; padding:10px 12px; border:1px solid #ddd; border-radius:8px;">
  <button id="archiveClear" type="button" style="padding:10px 12px; border:1px solid #ddd; border-radius:8px; background:#fff; cursor:pointer;">Clear</button>
</div>

<div style="display:flex; gap:10px; flex-wrap: wrap; margin: 10px 0 14px;">
  <button id="tabPublished" type="button" style="padding:8px 12px; border-radius:999px; border:1px solid #ddd; background:#f6f8fa; cursor:pointer;">Published</button>
  <button id="tabQueue" type="button" style="padding:8px 12px; border-radius:999px; border:1px solid #ddd; background:#fff; cursor:pointer;">Queue</button>
  <span id="queueMeta" style="align-self:center; color:#888; font-size:12px;"></span>
</div>

<div id="archiveActiveFilter" style="display:none; margin: 8px 0; padding: 8px 12px; border-radius: 8px; background: #f6f8fa; border: 1px solid #eee; font-size: 14px;"></div>

<table id="archiveTablePublished">
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

    <tr class="archiveRow archiveRowPublished"
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

{%- assign q = site.data.news_queue_public -%}
<table id="archiveTableQueue" style="display:none;">
  <thead>
    <tr>
      <th style="text-align:left;">Fetched</th>
      <th style="text-align:left;">Title</th>
      <th style="text-align:left;">Source</th>
      <th style="text-align:left;">Tags</th>
      <th style="text-align:right;">Score</th>
    </tr>
  </thead>
  <tbody>
  {%- if q and q.pending and q.pending.size > 0 -%}
    {%- for item in q.pending -%}
      {%- assign companies = item.companies | default: "" -%}
      {%- assign topics = item.topics | default: "" -%}
      {%- assign tag_str = "" -%}
      {%- if companies and companies.size > 0 -%}{%- assign tag_str = companies | join: " " -%}{%- endif -%}
      {%- if topics and topics.size > 0 -%}
        {%- assign topics_joined = topics | join: " " -%}
        {%- assign tag_str = tag_str | append: " " | append: topics_joined -%}
      {%- endif -%}
      <tr class="archiveRow archiveRowQueue"
          data-title="{{ item.title | escape | replace: '&amp;#8217;', '’' | replace: '&#8217;', '’' | replace: '&amp;rsquo;', '’' | replace: '&rsquo;', '’' | downcase }}"
          data-source="{{ item.source | default: '' | downcase }}"
          data-tags="{{ tag_str | downcase }}"
          data-score="{{ item.score | default: 0 | plus: 0 }}">
        <td style="white-space:nowrap;">{{ item.fetched_at | default: "" }}</td>
        <td>
          <a href="{{ item.url }}" target="_blank" rel="noopener">
            {{ item.title | escape | replace: '&amp;#8217;', '’' | replace: '&#8217;', '’' | replace: '&amp;rsquo;', '’' | replace: '&rsquo;', '’' }}
          </a>
        </td>
        <td style="white-space:nowrap;">{{ item.source | default: "" }}</td>
        <td>
          {%- if item.companies and item.companies.size > 0 -%}
            {%- for tag in item.companies -%}
              <button type="button" class="archiveTag" data-tag="{{ tag | downcase }}" style="margin:2px 4px 2px 0; padding:2px 8px; border-radius:999px; border:1px solid #eee; background:#f8f9fa; cursor:pointer; font-size:12px;">
                {{ tag }}
              </button>
            {%- endfor -%}
          {%- endif -%}
          {%- if item.topics and item.topics.size > 0 -%}
            {%- for tag in item.topics -%}
              <button type="button" class="archiveTag" data-tag="{{ tag | downcase }}" style="margin:2px 4px 2px 0; padding:2px 8px; border-radius:999px; border:1px solid #eee; background:#f8f9fa; cursor:pointer; font-size:12px;">
                {{ tag }}
              </button>
            {%- endfor -%}
          {%- endif -%}
        </td>
        <td style="text-align:right; font-variant-numeric: tabular-nums;">{{ item.score | default: 0 }}</td>
      </tr>
    {%- endfor -%}
  {%- else -%}
    <tr><td colspan="5" style="color:#888;">Queue data not available yet (wait for the next automation run).</td></tr>
  {%- endif -%}
  </tbody>
</table>

<p id="archiveCount" style="margin-top: 12px; color: #666;"></p>

<script>
  (function() {
    var searchEl = document.getElementById('archiveSearch');
    var clearEl = document.getElementById('archiveClear');
    var activeEl = document.getElementById('archiveActiveFilter');
    var tabPublished = document.getElementById('tabPublished');
    var tabQueue = document.getElementById('tabQueue');
    var tablePublished = document.getElementById('archiveTablePublished');
    var tableQueue = document.getElementById('archiveTableQueue');
    var queueMeta = document.getElementById('queueMeta');

    var activeTab = 'published';
    var activeTag = null;

    var rowsPublished = Array.from(document.querySelectorAll('.archiveRowPublished'));
    var rowsQueue = Array.from(document.querySelectorAll('.archiveRowQueue'));

    {% if q and q.updated_at_utc %}
      {% assign updated_epoch = q.updated_at_utc | date: "%s" | plus: 0 %}
      {% assign updated_ist_epoch = updated_epoch | plus: 19800 %}
      queueMeta.textContent = 'Queue updated: {{ updated_ist_epoch | date: "%b %-d, %Y %H:%M" }} IST';
    {% endif %}

    function applyFilter() {
      var q = (searchEl.value || '').trim().toLowerCase();
      var visible = 0;
      var rows = (activeTab === 'queue') ? rowsQueue : rowsPublished;

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

      document.getElementById('archiveCount').textContent = visible + ' shown';
    }

    function wireTagButtons() {
      document.querySelectorAll('.archiveTag').forEach(function(btn) {
        btn.addEventListener('click', function() {
          var t = btn.dataset.tag;
          activeTag = (activeTag === t) ? null : t;
          applyFilter();
        });
      });
    }

    function setTab(tab) {
      activeTab = tab;
      tabPublished.style.background = (tab === 'published') ? '#f6f8fa' : '#fff';
      tabQueue.style.background = (tab === 'queue') ? '#f6f8fa' : '#fff';
      tablePublished.style.display = (tab === 'published') ? '' : 'none';
      tableQueue.style.display = (tab === 'queue') ? '' : 'none';
      activeTag = null;
      applyFilter();
    }

    tabPublished.addEventListener('click', function() { setTab('published'); });
    tabQueue.addEventListener('click', function() { setTab('queue'); });

    searchEl.addEventListener('input', applyFilter);
    clearEl.addEventListener('click', function() {
      activeTag = null;
      searchEl.value = '';
      applyFilter();
    });

    wireTagButtons();
    setTab('published');
  })();
</script>
