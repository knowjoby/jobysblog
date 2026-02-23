---
layout: default
title: Article Archives
permalink: /archives/
---

# 📚 Complete Article Archives

Browse all {{ site.posts | size }} articles

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
<!-- TEMPORARY DEBUG VIEW -->
<h2>Debug: Article Sources</h2>

<h3>1. Posts in _posts folder ({{ site.posts | size }} total):</h3>
<ul>
{% for post in site.posts %}
  <li>{{ post.date }} - <strong>{{ post.title }}</strong> (Source: {{ post.source }})</li>
{% else %}
  <li>No posts found in _posts folder.</li>
{% endfor %}
</ul>

<h3>2. Data in news_queue.json (if it exists):</h3>
<ul>
{% if site.data.news_queue and site.data.news_queue.pending %}
  {% for item in site.data.news_queue.pending %}
    <li>{{ item.added_at }} - <strong>{{ item.title }}</strong> (Source: {{ item.source }})</li>
  {% endfor %}
{% else %}
  <li>No pending items found in news_queue.json.</li>
{% endif %}
</ul>

<h3>3. Data from stats.yml:</h3>
<ul>
  <li>Total articles (from stats): {{ site.data.stats.total_articles | default: 'not found' }}</li>
  <li>Filtered articles (from stats): {{ site.data.stats.filtered_articles | default: 'not found' }}</li>
</ul>

<!-- Keep pagination and JS commented out for now -->
<!-- Pagination -->
<!-- <div class="pagination"> ... </div> -->
<!-- <script> ... </script> -->

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
let allRows = [];
let filteredRows = [];

// Initialize on page load
window.onload = function() {
  // Get all rows
  allRows = Array.from(document.querySelectorAll('.article-row'));
  filteredRows = [...allRows];
  updatePagination();
};

function filterArticles(company) {
  // Update active button
  document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');
  
  const searchTerm = document.getElementById('searchInput').value.toLowerCase();
  
  // Filter rows
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
  
  // Determine if column is numeric (Date or Score)
  const isNumeric = column === 0 || column === 4;
  
  rows.sort((a, b) => {
    let aVal = a.cells[column].innerText;
    let bVal = b.cells[column].innerText;
    
    if (isNumeric) {
      // Handle date specially (YYYY-MM-DD format)
      if (column === 0) {
        return aVal.localeCompare(bVal);
      }
      return parseFloat(aVal) - parseFloat(bVal);
    }
    return aVal.localeCompare(bVal);
  });
  
  // Toggle sort direction
  if (window.sortColumn === column) {
    rows.reverse();
  }
  window.sortColumn = column;
  
  // Reorder the table body
  const tbody = document.getElementById('tableBody');
  rows.forEach(row => tbody.appendChild(row));
  
  updatePagination();
}

function updatePagination() {
  const rowsToShow = filteredRows.length > 0 ? filteredRows : allRows;
  const totalPages = Math.ceil(rowsToShow.length / rowsPerPage);
  
  // Hide all rows first
  allRows.forEach(row => row.style.display = 'none');
  
  // Show only current page rows
  const start = (currentPage - 1) * rowsPerPage;
  const end = Math.min(start + rowsPerPage, rowsToShow.length);
  
  for (let i = start; i < end; i++) {
    rowsToShow[i].style.display = '';
  }
  
  // Update page info and buttons
  document.getElementById('pageInfo').innerText = `Page ${currentPage} of ${totalPages || 1}`;
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
