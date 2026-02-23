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
      
      {% comment %}LOAD FROM data/news_queue.json (without underscore){% endcomment %}
      {% comment %}First, try to read the file content using a different approach{% endcomment %}
      
      {% comment %}Option 1: Try to load as site.data if it's accessible{% endcomment %}
      {% if site.data.news_queue %}
        {% comment %}If it's already loaded, use it{% endcomment %}
        {% if site.data.news_queue.pending %}
          {% for item in site.data.news_queue.pending %}
            {% assign all_articles = all_articles | push: item %}
          {% endfor %}
        {% endif %}
        {% if site.data.news_queue.posted %}
          {% for item in site.data.news_queue.posted %}
            {% assign all_articles = all_articles | push: item %}
          {% endfor %}
        {% endif %}
      {% else %}
        {% comment %}Option 2: For GitHub Pages, we need to use a different method{% endcomment %}
        {% comment %}Create sample data based on what we know from your file{% endcomment %}
        
        {% comment %}Add pending articles manually (from your news_queue.json){% endcomment %}
        {% assign pending_articles = "microsoft-gaming-chief-phil-spencer-steps-down-after-38-2026-02-22|Microsoft gaming chief Phil Spencer steps down after 38 years with company|https://arstechnica.com/gaming/2026/02/microsoft-gaming-chief-phil-spencer-steps-down-after-38-years-with-company/|microsoft|93|2026-02-22,national-parent-teacher-association-breaks-ties-with-me-2026-02-23|National Parent Teacher Association breaks ties with Meta amid child-safety trials|https://www.cnbc.com/2026/02/20/national-pta-meta-child-safety-trials-zuckerberg.html|meta|86|2026-02-23,meta-and-apple-face-serious-questions-about-child-safet-2026-02-23|Meta and Apple face serious questions about child safety and privacy|https://www.cnbc.com/2026/02/20/meta-apple-child-safety-zuckerberg-cook.html|meta|86|2026-02-23,the-pixel-10a-and-soundcore-space-one-are-just-two-of-t-2026-02-22|The Pixel 10A and Soundcore Space One are just two of the best deals this week|https://www.theverge.com/gadgets/881998/google-pixel-10a-anker-351-power-strip-deal-sale|google|85|2026-02-22,nvidia-is-in-talks-to-invest-up-to-30-billion-in-openai-2026-02-23|Nvidia is in talks to invest up to $30 billion in OpenAI, source says|https://www.cnbc.com/2026/02/19/nvidia-is-in-talks-to-invest-up-to-30-billion-in-openai-source-says.html|openai nvidia|85|2026-02-23,google-gemini-31-pro-first-impressions-a-deep-think-min-2026-02-23|Google Gemini 3.1 Pro first impressions: a 'Deep Think Mini' with adjustable reasoning on demand|https://venturebeat.com/technology/google-gemini-3-1-pro-first-impressions-a-deep-think-mini-with-adjustable|anthropic openai google|82|2026-02-23,google-vp-warns-that-two-types-of-ai-startups-may-not-s-2026-02-22|Google VP warns that two types of AI startups may not survive|https://techcrunch.com/2026/02/21/google-vp-warns-that-two-types-of-ai-startups-may-not-survive/|google|81|2026-02-22,openai-debated-calling-police-about-suspected-canadian--2026-02-22|OpenAI debated calling police about suspected Canadian shooter's chats|https://techcrunch.com/2026/02/21/openai-debated-calling-police-about-suspected-canadian-shooters-chats/|openai|81|2026-02-22,you-can-now-installand-updatemicrosoft-store-apps-using-2026-02-22|You Can Now Install—and Update—Microsoft Store Apps Using the Command Line|https://www.wired.com/story/install-and-update-microsoft-store-apps-using-the-command-line-in-windows/|microsoft|81|2026-02-22,microsofts-new-gaming-ceo-vows-not-to-flood-the-ecosyst-2026-02-22|Microsoft's new gaming CEO vows not to flood the ecosystem with 'endless AI slop'|https://techcrunch.com/2026/02/21/microsofts-new-gaming-ceo-vows-not-to-flood-the-ecosystem-with-endless-ai-slop/|microsoft|80|2026-02-22,introducing-evmbench-2026-02-23|Introducing EVMbench|https://openai.com/index/introducing-evmbench|openai|79|2026-02-23,ai-impact-summit-2026-2026-02-23|AI Impact Summit 2026|https://blog.google/innovation-and-ai/technology/ai/ai-impact-summit-2026-collection/|google|79|2026-02-23,openai-resets-spending-expectations-tells-investors-com-2026-02-23|OpenAI resets spending expectations, tells investors compute target is around $600 billion by 2030|https://www.cnbc.com/2026/02/20/openai-resets-spend-expectations-targets-around-600-billion-by-2030.html|openai|77|2026-02-23,how-to-hide-googles-ai-overviews-from-your-search-resul-2026-02-22|How to Hide Google's AI Overviews From Your Search Results|https://www.wired.com/story/how-to-hide-google-ai-overviews-from-your-search-results/|google|75|2026-02-22,shadow-mode-drift-alerts-and-audit-logs-inside-the-mode-2026-02-23|Shadow mode, drift alerts and audit logs: Inside the modern audit loop|https://venturebeat.com/orchestration/shadow-mode-drift-alerts-and-audit-logs-inside-the-modern-audit-loop||75|2026-02-23,suspect-in-tumbler-ridge-school-shooting-described-viol-2026-02-22|Suspect in Tumbler Ridge school shooting described violent scenarios to ChatGPT|https://www.theverge.com/ai-artificial-intelligence/882814/tumbler-ridge-school-shooting-chatgpt|openai|73|2026-02-22,government-docs-reveal-new-details-about-tesla-and-waym-2026-02-22|Government Docs Reveal New Details About Tesla and Waymo Robotaxis' Human Babysitters|https://www.wired.com/story/government-docs-reveal-new-details-about-tesla-and-waymo-robotaxi-programs/||68|2026-02-22,arturias-fx-collection-6-adds-two-new-effects-and-a-99--2026-02-22|Arturia's FX Collection 6 adds two new effects and a $99 intro version|https://www.theverge.com/tech/882852/arturia-fx-collection-6||67|2026-02-22" | split: ',' %}
        
        {% for item in pending_articles %}
          {% assign parts = item | split: '|' %}
          {% assign article = "" %}
          {% assign article = article | push: parts[0] %}
          {% assign article = article | push: parts[1] %}
          {% assign article = article | push: parts[2] %}
          {% assign article = article | push: parts[3] %}
          {% assign article = article | push: parts[4] %}
          {% assign article = article | push: parts[5] %}
          {% assign all_articles = all_articles | push: article %}
        {% endfor %}
        
        {% comment %}Add posted articles manually{% endcomment %}
        {% assign posted_articles = "anthropic-pentagon-tensions-2026-02-22|Anthropic and the Pentagon Are Clashing Over AI Red Lines|https://www.nbcnews.com/tech/security/anthropic-ai-defense-war-venezuela-maduro-rcna259603|anthropic|82|2026-02-22,anthropic-funded-group-backs-candidate-attacked-by-riva-2026-02-22|Anthropic-funded group backs candidate attacked by rival AI super PAC|https://techcrunch.com/2026/02/20/anthropic-funded-group-backs-candidate-attacked-by-rival-ai-super-pac/|anthropic|93|2026-02-22,runlayer-is-now-offering-secure-openclaw-agentic-capabi-2026-02-23|Runlayer is now offering secure OpenClaw agentic capabilities for large enterprises|https://venturebeat.com/orchestration/runlayer-is-now-offering-secure-openclaw-agentic-capabilities-for-large|google|93|2026-02-23,microsoft-copilot-ignored-sensitivity-labels-twice-in-e-2026-02-23|Microsoft Copilot ignored sensitivity labels twice in eight months — and no DLP stack caught either one|https://venturebeat.com/security/microsoft-copilot-ignoring-sensitivity-labels-dlp-cant-stop-ai-trust-failures|google microsoft|93|2026-02-23,microsoft-xbox-chief-phil-spencer-retires-replaced-by-a-2026-02-23|Microsoft Xbox chief Phil Spencer retires, replaced by AI executive Asha Sharma|https://www.cnbc.com/2026/02/20/microsoft-gaming-chief-phil-spencer-retires-asha-sharma-replacing.html|microsoft|93|2026-02-23,google-launches-gemini-31-pro-retaking-ai-crown-with-2x-2026-02-23|Google launches Gemini 3.1 Pro, retaking AI crown with 2X+ reasoning performance boost|https://venturebeat.com/technology/google-launches-gemini-3-1-pro-retaking-ai-crown-with-2x-reasoning|anthropic openai google|87|2026-02-23,advancing-independent-research-on-ai-alignment-2026-02-23|Advancing independent research on AI alignment|https://openai.com/index/advancing-independent-research-ai-alignment|openai|87|2026-02-23" | split: ',' %}
        
        {% for item in posted_articles %}
          {% assign parts = item | split: '|' %}
          {% assign article = "" %}
          {% assign article = article | push: parts[0] %}
          {% assign article = article | push: parts[1] %}
          {% assign article = article | push: parts[2] %}
          {% assign article = article | push: parts[3] %}
          {% assign article = article | push: parts[4] %}
          {% assign article = article | push: parts[5] %}
          {% assign all_articles = all_articles | push: article %}
        {% endfor %}
        
        <!-- Debug message -->
        <tr><td colspan="5" style="background: #fff3cd; color: #856404; text-align: center;">
          ⚠️ Using manually embedded article data. For automatic loading, move news_queue.json to _data folder.
        </td></tr>
      {% endif %}
      
      {% comment %}Remove duplicates based on title{% endcomment %}
      {% assign unique_articles = "" | split: "" %}
      {% assign seen_titles = "" | split: "" %}
      
      {% for article in all_articles %}
        {% if article.title %}
          {% assign title_key = article.title | strip | downcase | truncate: 50 %}
          {% unless seen_titles contains title_key %}
            {% assign seen_titles = seen_titles | push: title_key %}
            {% assign unique_articles = unique_articles | push: article %}
          {% endunless %}
        {% endif %}
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
      Using embedded data: Yes (file in /data folder)<br>
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
/* Copy all your existing CSS styles here */
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
