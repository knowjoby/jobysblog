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
<!-- DEBUG SECTION - REMOVE LATER -->
<div style="background: #fff3cd; padding: 15px; margin: 20px 0; border: 1px solid #ffeeba; border-radius: 4px;">
  <strong>🔍 Debug Information:</strong><br>
  Total posts in site: {{ site.posts | size }}<br>
  <hr>
  <strong>First 3 post titles (if any):</strong><br>
  {% for post in site.posts limit:3 %}
    - {{ post.title }} ({{ post.date }})<br>
  {% else %}
    No posts found!<br>
  {% endfor %}
</div>
<!-- END DEBUG SECTION -->
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
    <tbody>
      {% assign all_articles = "" | split: "" %}
      
      {% comment %}Get articles from posted posts{% endcomment %}
      {% for post in site.posts %}
        {% if post.tags contains 'ai-news' or post.categories contains 'ai-news' %}
          {% assign article = post %}
          {% assign all_articles = all_articles | push: article %}
        {% endif %}
      {% endfor %}
      
      {% comment %}Also get articles from news_queue.json pending items{% endcomment %}
      {% if site.data.news_queue and site.data.news_queue.pending %}
        {% for item in site.data.news_queue.pending %}
          {% assign all_articles = all_articles | push: item %}
        {% endfor %}
      {% endif %}
      
      {% comment %}Sort by date (newest first){% endcomment %}
      {% assign sorted_articles = all_articles | sort: "date" | reverse %}
      
      {% for article in sorted_articles limit:200 %}
      <tr class="article-row" 
          data-companies="{% if article.companies %}{{ article.companies | join: ' ' }}{% elsif article.tags %}{{ article.tags | join: ' ' }}{% endif %}"
          data-title="{{ article.title | downcase }}"
          data-source="{{ article.source | downcase }}">
        <td>{% if article.date %}{{ article.date | date: '%Y-%m-%d' }}{% elsif article.added_at %}{{ article.added_at }}{% endif %}</td>
        <td><a href="{% if article.link %}{{ article.link }}{% elsif article.source_url %}{{ article.source_url }}{% endif %}" target="_blank">{{ article.title }}</a></td>
        <td>{% if article.source %}{{ article.source }}{% endif %}</td>
        <td class="company-tags">
          {% if article.companies %}
            {% for company in article.companies %}
              <span class="company-tag {{ company }}">{{ company | capitalize }}</span>
            {% endfor %}
          {% elsif article.tags %}
            {% for tag in article.tags %}
              {% if tag == 'openai' or tag == 'anthropic' or tag == 'google' or tag == 'microsoft' or tag == 'meta' or tag == 'deepseek' %}
                <span class="company-tag {{ tag }}">{{ tag | capitalize }}</span>
              {% endif %}
            {% endfor %}
          {% endif %}
        </td>
        <td class="score-cell">
          <span class="score-badge 
            {% if article.score >= 85 %}score-high
            {% elsif article.score >= 70 %}score-medium
            {% else %}score-low{% endif %}">
            {{ article.score }}
          </span>
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>

<!-- Pagination -->
<div class="pagination">
  <button onclick="previousPage()" id="prevBtn">← Previous</button>
  <span id="pageInfo">Page 1</span>
  <button onclick="nextPage()" id="nextBtn">Next →</button>
</div>

<!-- JavaScript for filtering, sorting, and pagination -->
<script>
let currentPage = 1;
const rowsPerPage = 20;
let filteredRows = [];

function filterArticles(company) {
  // Update active button
  document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');
  
  const rows = document.querySelectorAll('.article-row');
  const searchTerm = document.getElementById('searchInput').value.toLowerCase();
  
  filteredRows = [];
  rows.forEach(row => {
    const companies = row.getAttribute('data-companies') || '';
    const title = row.getAttribute('data-title') || '';
    const source = row.getAttribute('data-source') || '';
    
    const matchesCompany = company === 'all' || companies.includes(company);
    const matchesSearch = searchTerm === '' || 
                         title.includes(searchTerm) || 
                         source.includes(searchTerm);
    
    if (matchesCompany && matchesSearch) {
      filteredRows.push(row);
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
  
  currentPage = 1;
  updatePagination();
}

function searchArticles() {
  const activeFilter = document.querySelector('.filter-btn.active')?.innerText.toLowerCase() || 'all';
  filterArticles(activeFilter);
}

function sortTable(column) {
  const table = document.getElementById('articlesTable');
  const tbody = table.tBodies[0];
  const rows = Array.from(tbody.rows);
  
  const isNumeric = column === 0 || column === 4; // Date or Score columns
  
  rows.sort((a, b) => {
    let aVal = a.cells[column].innerText;
    let bVal = b.cells[column].innerText;
    
    if (isNumeric) {
      return parseFloat(aVal) - parseFloat(bVal);
    }
    return aVal.localeCompare(bVal);
  });
  
  // Reverse if already sorted
  if (table.sortColumn === column) {
    rows.reverse();
    table.sortDirection = table.sortDirection === 'asc' ? 'desc' : 'asc';
  } else {
    table.sortColumn = column;
    table.sortDirection = 'asc';
  }
  
  tbody.append(...rows);
}

function updatePagination() {
  const visibleRows = filteredRows.length > 0 ? filteredRows : 
                     Array.from(document.querySelectorAll('.article-row')).filter(r => r.style.display !== 'none');
  
  const totalPages = Math.ceil(visibleRows.length / rowsPerPage);
  
  // Hide all rows first
  document.querySelectorAll('.article-row').forEach(r => r.style.display = 'none');
  
  // Show only current page rows
  const start = (currentPage - 1) * rowsPerPage;
  const end = start + rowsPerPage;
  
  visibleRows.slice(start, end).forEach(r => r.style.display = '');
  
  document.getElementById('pageInfo').innerText = `Page ${currentPage} of ${totalPages}`;
  document.getElementById('prevBtn').disabled = currentPage === 1;
  document.getElementById('nextBtn').disabled = currentPage === totalPages;
}

function previousPage() {
  if (currentPage > 1) {
    currentPage--;
    updatePagination();
  }
}

function nextPage() {
  const visibleRows = filteredRows.length > 0 ? filteredRows : 
                     Array.from(document.querySelectorAll('.article-row')).filter(r => r.style.display !== 'none');
  const totalPages = Math.ceil(visibleRows.length / rowsPerPage);
  
  if (currentPage < totalPages) {
    currentPage++;
    updatePagination();
  }
}

// Initialize on load
window.onload = function() {
  filterArticles('all');
};
</script>

<!-- Add some CSS -->
<style>
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
