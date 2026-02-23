---
layout: default
title: Article Archives
permalink: /archives/
---

# 📚 Complete Article Archives

Browse all {{ site.data.stats.total_articles | default: 127 }} articles discovered from {{ site.data.stats.total_sources | default: 15 }} sources. Filtered down to {{ site.data.stats.filtered_articles | default: 42 }} relevant AI news items.

<!-- Filters -->
<div class="filters">
  <button class="filter-btn active" onclick="filterArticles('all')">All</button>
  <button class="filter-btn" onclick="filterArticles('openai')">OpenAI</button>
  <button class="filter-btn" onclick="filterArticles('anthropic')">Anthropic</button>
  <button class="filter-btn" onclick="filterArticles('google')">Google</button>
  <button class="filter-btn" onclick="filterArticles('microsoft')">Microsoft</button>
  <button class="filter-btn" onclick="filterArticles('meta')">Meta</button>
  <button class="filter-btn" onclick="filterArticles('deepseek')">DeepSeek</button>
</div>

<!-- Search Box -->
<div class="search-box">
  <input type="text" id="searchInput" placeholder="Search articles..." onkeyup="searchArticles()">
</div>

<!-- Articles Table -->
<div class="archives-table">
  <table id="articlesTable">
    <thead>
      <tr>
        <th onclick="sortTable(0)">Date ⬍</th>
        <th onclick="sortTable(1)">Title ⬍</th>
        <th onclick="sortTable(2)">Source ⬍</th>
        <th onclick="sortTable(3)">Companies ⬍</th>
        <th onclick="sortTable(4)">Score ⬍</th>
      </tr>
    </thead>
    <tbody id="tableBody">
      {% assign all_articles = "" | split: "" %}
      
      {% comment %}LOAD FROM _POSTS FOLDER (your 9 articles){% endcomment %}
      {% for post in site.posts %}
        {% assign all_articles = all_articles | push: post %}
      {% endfor %}
      
      {% comment %}LOAD FROM NEWS_QUEUE.JSON - Using site.data.news_queue directly{% endcomment %}
      {% if site.data.news_queue %}
        {% comment %}Load pending articles{% endcomment %}
        {% if site.data.news_queue.pending %}
          {% for item in site.data.news_queue.pending %}
            {% assign all_articles = all_articles | push: item %}
          {% endfor %}
        {% endif %}
        
        {% comment %}Load posted articles{% endcomment %}
        {% if site.data.news_queue.posted %}
          {% for item in site.data.news_queue.posted %}
            {% assign all_articles = all_articles | push: item %}
          {% endfor %}
        {% endif %}
      {% else %}
        <!-- Debug: news_queue.json not loaded -->
        <tr><td colspan="5" style="background: #ffebee; color: #c62828; text-align: center;">
          ⚠️ news_queue.json not found. Make sure it's in the _data folder.
        </td></tr>
      {% endif %}
      
      {% comment %}Remove duplicates based on title{% endcomment %}
      {% assign unique_articles = "" | split: "" %}
      {% assign seen_titles = "" | split: "" %}
      
      {% for article in all_articles %}
        {% assign title_key = article.title | strip | downcase | truncate: 50 %}
        {% unless seen_titles contains title_key %}
          {% assign seen_titles = seen_titles | push: title_key %}
          {% assign unique_articles = unique_articles | push: article %}
        {% endunless %}
      {% endfor %}
      
      {% comment %}Sort by date (newest first){% endcomment %}
      {% assign sorted_articles = unique_articles | sort: "added_at" | reverse %}
      
      {% if sorted_articles.size == 0 %}
        <tr><td colspan="5" style="text-align: center; padding: 40px;">No articles found</td></tr>
      {% else %}
        {% for article in sorted_articles %}
        <tr class="article-row" 
            data-companies="{% if article.companies %}{% for company in article.companies %}{{ company | downcase }} {% endfor %}{% endif %}"
            data-title="{{ article.title | downcase | escape }}"
            data-source="
              {% if article.source %}
                {{ article.source | downcase | escape }}
              {% elsif article.source_url %}
                {{ article.source_url | downcase | escape }}
              {% endif %}">
          <td>
            {% if article.added_at %}
              {{ article.added_at }}
            {% elsif article.date %}
              {{ article.date | date: '%Y-%m-%d' }}
            {% else %}
              No date
            {% endif %}
          </td>
          <td>
            <a href="
              {% if article.source_url %}
                {{ article.source_url }}
              {% elsif article.link %}
                {{ article.link }}
              {% elsif article.url %}
                {{ article.url }}
              {% else %}
                #
              {% endif %}" target="_blank">
              {{ article.title }}
            </a>
          </td>
          <td>
            {% if article.source %}
              {{ article.source }}
            {% elsif article.source_url %}
              {% assign url_parts = article.source_url | split: '/' %}
              {{ url_parts[2] | replace: 'www.', '' | truncate: 20 }}
            {% else %}
              Unknown
            {% endif %}
          </td>
          <td class="company-tags">
            {% if article.companies %}
              {% for company in article.companies %}
                <span class="company-tag {{ company | downcase }}">{{ company | capitalize }}</span>
              {% endfor %}
            {% endif %}
          </td>
          <td class="score-cell">
            <span class="score-badge 
              {% if article.score >= 85 %}score-high
              {% elsif article.score >= 70 %}score-medium
              {% else %}score-low{% endif %}">
              {{ article.score | default: 'N/A' }}
            </span>
          </td>
        </tr>
        {% endfor %}
      {% endif %}
    </tbody>
  </table>
</div>

<!-- Pagination -->
<div class="pagination">
  <button onclick="previousPage()" id="prevBtn">← Previous</button>
  <span id="pageInfo">Page 1</span>
  <button onclick="nextPage()" id="nextBtn">Next →</button>
</div>

<!-- Article count and debug info -->
<div style="margin: 20px 0; padding: 15px; background: #f5f5f5; border-radius: 4px;">
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <div>
      <strong>📊 Statistics:</strong><br>
      Total articles loaded: <span id="totalCount">0</span><br>
      Showing page: <span id="pageDisplay"></span>
    </div>
    <div style="text-align: right;">
      <strong>🔧 Debug Info:</strong><br>
      Posts folder: {{ site.posts | size }} articles<br>
      News queue loaded: {% if site.data.news_queue %}✅ Yes{% else %}❌ No{% endif %}<br>
      Pending items: {% if site.data.news_queue.pending %}{{ site.data.news_queue.pending | size }}{% else %}0{% endif %}<br>
      Posted items: {% if site.data.news_queue.posted %}{{ site.data.news_queue.posted | size }}{% else %}0{% endif %}
    </div>
  </div>
</div>

<script>
let currentPage = 1;
const rowsPerPage = 20;
let allRows = [];
let filteredRows = [];

window.onload = function() {
  allRows = Array.from(document.querySelectorAll('.article-row'));
  filteredRows = [...allRows];
  document.getElementById('totalCount').innerText = allRows.length;
  updatePagination();
};

function filterArticles(company) {
  document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');
  
  const searchTerm = document.getElementById('searchInput').value.toLowerCase();
  
  filteredRows = allRows.filter(row => {
    const companies = row.getAttribute('data-companies') || '';
    const title = row.getAttribute('data-title') || '';
    const source = row.getAttribute('data-source') || '';
    
    const matchesCompany = company === 'all' || companies.includes(company.toLowerCase());
    const matchesSearch = searchTerm === '' || 
                         title.includes(searchTerm) || 
                         source.includes(searchTerm);
    
    return matchesCompany && matchesSearch;
  });
  
  currentPage = 1;
  updatePagination();
}

function searchArticles() {
  const activeFilter = document.querySelector('.filter-btn.active')?.innerText.toLowerCase() || 'all';
  filterArticles(activeFilter);
}

function sortTable(column) {
  const rows = filteredRows.length > 0 ? filteredRows : allRows;
  const isNumeric = column === 0 || column === 4;
  
  rows.sort((a, b) => {
    let aVal = a.cells[column].innerText;
    let bVal = b.cells[column].innerText;
    
    if (isNumeric) {
      if (column === 0) {
        return bVal.localeCompare(aVal);
      }
      return parseFloat(bVal) - parseFloat(aVal);
    }
    return aVal.localeCompare(bVal);
  });
  
  if (window.sortColumn === column) {
    rows.reverse();
  }
  window.sortColumn = column;
  
  const tbody = document.getElementById('tableBody');
  rows.forEach(row => tbody.appendChild(row));
  
  updatePagination();
}

function updatePagination() {
  const rowsToShow = filteredRows.length > 0 ? filteredRows : allRows;
  const totalPages = Math.ceil(rowsToShow.length / rowsPerPage);
  
  allRows.forEach(row => row.style.display = 'none');
  
  const start = (currentPage - 1) * rowsPerPage;
  const end = Math.min(start + rowsPerPage, rowsToShow.length);
  
  for (let i = start; i < end; i++) {
    rowsToShow[i].style.display = '';
  }
  
  document.getElementById('pageInfo').innerText = `Page ${currentPage} of ${totalPages || 1}`;
  document.getElementById('pageDisplay').innerText = `${currentPage} of ${totalPages || 1}`;
  document.getElementById('prevBtn').disabled = currentPage === 1;
  document.getElementById('nextBtn').disabled = currentPage === totalPages || totalPages === 0;
}

function previousPage() {
  if (currentPage > 1) {
    currentPage--;
    updatePagination();
  }
}

function nextPage() {
  const rowsToShow = filteredRows.length > 0 ? filteredRows : allRows;
  const totalPages = Math.ceil(rowsToShow.length / rowsPerPage);
  
  if (currentPage < totalPages) {
    currentPage++;
    updatePagination();
  }
}
</script>

<style>
/* Keep all your existing CSS styles */
.filters {
  margin: 20px 0;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.filter-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
}
.filter-btn:hover {
  background: #f0f0f0;
}
.filter-btn.active {
  background: #0366d6;
  color: white;
  border-color: #0366d6;
}
.search-box {
  margin: 20px 0;
}
.search-box input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}
.archives-table {
  overflow-x: auto;
  margin: 20px 0;
}
.archives-table table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}
.archives-table th {
  background: #f5f5f5;
  padding: 12px;
  text-align: left;
  cursor: pointer;
  border-bottom: 2px solid #ddd;
}
.archives-table th:hover {
  background: #e8e8e8;
}
.archives-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #eee;
}
.archives-table tr:hover {
  background: #f9f9f9;
}
.company-tag {
  display: inline-block;
  padding: 2px 8px;
  margin: 2px;
  border-radius: 12px;
  font-size: 12px;
  background: #e8f4fe;
  color: #0366d6;
}
.company-tag.openai { background: #e3f2e3; color: #2e7d32; }
.company-tag.anthropic { background: #f3e5f5; color: #7b1fa2; }
.company-tag.google { background: #fff3e0; color: #bf360c; }
.company-tag.microsoft { background: #e3f2fd; color: #0d47a1; }
.company-tag.meta { background: #e8eaf6; color: #1a237e; }
.company-tag.deepseek { background: #fce4ec; color: #880e4f; }
.score-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: bold;
  font-size: 12px;
}
.score-high {
  background: #c8e6c9;
  color: #2e7d32;
}
.score-medium {
  background: #fff3e0;
  color: #bf360c;
}
.score-low {
  background: #ffebee;
  color: #c62828;
}
.pagination {
  margin: 20px 0;
  display: flex;
  justify-content: center;
  gap: 10px;
  align-items: center;
}
.pagination button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}
.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.pagination button:hover:not(:disabled) {
  background: #f0f0f0;
}
</style>
