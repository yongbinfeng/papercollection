---
layout: default
---

<style>
  html { scroll-behavior: smooth; }
  header { display: none !important; }
  footer { display: none !important; }
  section { width: 100% !important; max-width: 1000px !important; float: none !important; margin: 0 auto !important; padding-top: 40px !important; }
  .wrapper { width: 95% !important; max-width: 1100px !important; }

  .category-nav { 
    display: flex; 
    flex-wrap: wrap; 
    gap: 10px; 
    margin-bottom: 30px; 
    position: sticky; 
    top: 0; 
    background: rgba(255, 255, 255, 0.95); /* Slight transparency */
    padding: 15px 0; 
    z-index: 100; 
    border-bottom: 1px solid #eaeaea;
  }
  .category-nav a { 
    background-color: #f0fdfa; /* Very light teal */
    color: #0f766e; /* Teal */
    padding: 8px 16px; 
    border-radius: 20px; 
    text-decoration: none; 
    font-size: 0.9em; 
    font-weight: bold; 
    border: 1px solid #ccfbf1; 
    transition: all 0.2s ease; 
  }
  .category-nav a:hover { 
    background-color: #0f766e; 
    color: white;
    text-decoration: none; 
  }

  #backToTopBtn { display: none; position: fixed; bottom: 30px; right: 30px; z-index: 99; font-size: 15px; font-weight: bold; border: none; outline: none; background-color: #0366d6; color: white; cursor: pointer; padding: 12px 18px; border-radius: 50px; box-shadow: 0px 4px 10px rgba(0,0,0,0.2); transition: background-color 0.3s; }
  #backToTopBtn:hover { background-color: #0056b3; }

  #searchInput:focus {
    border-color: #0f766e;
    box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.15);
  }

  /* Styling to make Markdown bullet points look clean inside notes */
  .paper-notes p { margin-top: 4px; margin-bottom: 8px; }
  .paper-notes ul { margin-top: 4px; margin-bottom: 8px; padding-left: 20px; }
</style>

<script>
  MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']],
      displayMath: [['$$', '$$'], ['\\[', '\\]']]
    }
  };
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>

# Some Fun Papers

A collection of papers I find interesting and want to keep handy for future reference, with some notes quickly taken.

<p style="font-size: 0.85em; color: #666; margin-top: -10px; margin-bottom: 25px;"><em>Last updated: {{ site.time | date: "%B %-d, %Y" }}</em></p>

<div style="position: relative; margin-bottom: 30px; width: 100%;">
  <span style="position: absolute; left: 16px; top: 14px; color: #9ca3af; font-size: 16px; pointer-events: none;">🔍</span>
  
  <input type="text" id="searchInput" onkeyup="searchPapers()" placeholder="Search publications by title, author, or keyword..." aria-label="Search publications" style="width: 100%; padding: 14px 20px 14px 45px; border: 1px solid #d1d5da; border-radius: 8px; font-size: 16px; transition: all 0.2s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.02); box-sizing: border-box; outline: none;">
</div>

<div id="noResultsMessage" style="display: none; text-align: center; padding: 40px 20px; color: #6b7280; font-size: 1.1em; background: #f9fafb; border-radius: 8px; border: 1px dashed #d1d5da; margin-bottom: 30px;">
  No publications found matching your search.
</div>

<div class="category-nav">
{% for dataset in site.data %}
  {% assign category_slug = dataset[0] %}
  {% if category_slug == 'dream_publications' %}{% continue %}{% endif %}
  {% assign category_name = category_slug | replace: '_', ' ' | capitalize %}
  {% if category_slug == 'generic_detector_rd' %}{% assign category_name = 'Generic Detector R&D' %}{% endif %}
  <a href="#{{ category_slug }}">{{ category_name }}</a>
{% endfor %}
</div>

<div id="paperList">
{% for dataset in site.data %}
  {% assign category_slug = dataset[0] %}
  {% if category_slug == 'dream_publications' %}{% continue %}{% endif %}
  {% assign category_papers = dataset[1] %}
  {% assign category_name = category_slug | replace: '_', ' ' | capitalize %}
  {% if category_slug == 'generic_detector_rd' %}{% assign category_name = 'Generic Detector R&D' %}{% endif %}

  <div class="category-section" id="{{ category_slug }}">
    <h2>{{ category_name }}</h2>
    <ul style="list-style-type: none; padding-left: 0;">
    
    {% assign sorted_papers = category_papers | sort: "year" | reverse %}
    
    {% for paper in sorted_papers %}
      <li class="paper-item" style="margin-bottom: 15px; padding: 15px; border: 1px solid #eaeaea; border-radius: 6px; background-color: #fcfcfc;">
        <strong style="font-size: 1.1em;">
          <a href="{{ paper.url }}" target="_blank" class="paper-title">{{ paper.title }}</a>
        </strong> ({{ paper.year }})<br>
        
        {% if paper.authors or paper.journal %}
          <div style="font-size: 0.9em; color: #555; margin-top: 5px; margin-bottom: 5px;">
            {% if paper.authors %}<em>{{ paper.authors }}</em>{% endif %}
            {% if paper.authors and paper.journal %}<br>{% endif %}
            {% if paper.journal %}Published in: {{ paper.journal }}{% endif %}
          </div>
        {% endif %}

        {% if paper.notes %}
          <div class="paper-notes" style="margin-top: 8px; font-size: 0.95em; color: #555;">
            <strong>Notes:</strong> 
            
            <div style="margin-left: 20px;">
              {{ paper.notes | markdownify }}
            </div>
            
          </div>
        {% endif %}
        
      </li>
    {% endfor %}
    </ul>
  </div>
{% endfor %}
</div>

<button onclick="scrollToTop()" id="backToTopBtn" title="Go to top">↑ Top</button>

<script>
function searchPapers() {
    let input = document.getElementById('searchInput').value.toLowerCase();
    let paperItems = document.getElementsByClassName('paper-item');
    let categorySections = document.getElementsByClassName('category-section');

    for (let i = 0; i < paperItems.length; i++) {
        let text = paperItems[i].innerText.toLowerCase();
        if (text.includes(input)) {
            paperItems[i].style.display = "";
        } else {
            paperItems[i].style.display = "none";
        }
    }

    for (let j = 0; j < categorySections.length; j++) {
        let visibleItems = categorySections[j].querySelectorAll('.paper-item:not([style*="display: none"])');
        if (visibleItems.length === 0) {
            categorySections[j].style.display = "none";
        } else {
            categorySections[j].style.display = "";
        }
    }
}

let topButton = document.getElementById("backToTopBtn");
window.onscroll = function() {
  if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
    topButton.style.display = "block";
  } else {
    topButton.style.display = "none";
  }
};

function scrollToTop() {
  document.body.scrollTop = 0; 
  document.documentElement.scrollTop = 0; 
}
</script>