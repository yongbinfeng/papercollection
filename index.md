---
layout: default
---

<style>
  /* Smooth scrolling for the jump links and back-to-top */
  html {
    scroll-behavior: smooth;
  }

  /* Hide the left sidebar entirely */
  header {
    display: none !important;
  }
  
  /* Hide the default footer */
  footer {
    display: none !important;
  }
  
  /* Expand the right content area to take up the full width */
  section {
    width: 100% !important;
    max-width: 1000px !important; 
    float: none !important;
    margin: 0 auto !important;
    padding-top: 40px !important;
  }
  
  /* Allow the main container to stretch */
  .wrapper {
    width: 95% !important;
    max-width: 1100px !important;
  }

  /* Styling for the Category Navigation Bar */
  .category-nav {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 30px;
  }
  
  .category-nav a {
    background-color: #f0f4f8;
    color: #0366d6;
    padding: 8px 16px;
    border-radius: 20px;
    text-decoration: none;
    font-size: 0.9em;
    font-weight: bold;
    border: 1px solid #d1d5da;
    transition: background-color 0.2s ease;
  }
  
  .category-nav a:hover {
    background-color: #e1e4e8;
    text-decoration: none;
  }

  /* Styling for the Back to Top Button */
  #backToTopBtn {
    display: none; /* Hidden by default */
    position: fixed; 
    bottom: 30px; 
    right: 30px; 
    z-index: 99; 
    font-size: 15px;
    font-weight: bold;
    border: none; 
    outline: none; 
    background-color: #0366d6; 
    color: white; 
    cursor: pointer; 
    padding: 12px 18px; 
    border-radius: 50px; /* Makes it a nice pill shape */
    box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    transition: background-color 0.3s;
  }

  #backToTopBtn:hover {
    background-color: #0056b3; 
  }
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

A collection of papers I find interesting and want to keep handy for future reference.

<p style="font-size: 0.85em; color: #666; margin-top: -10px; margin-bottom: 25px;"><em>Last updated: {{ site.time | date: "%B %-d, %Y" }}</em></p>

<input type="text" id="searchInput" onkeyup="searchPapers()" placeholder="Search for papers..." style="width: 100%; padding: 12px; margin-bottom: 20px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px;">

<div class="category-nav">
{% for dataset in site.data %}
  {% assign category_slug = dataset[0] %}
  {% assign category_name = category_slug | replace: '_', ' ' | capitalize %}
  <a href="#{{ category_slug }}">{{ category_name }}</a>
{% endfor %}
</div>

<div id="paperList">

{% for dataset in site.data %}
  {% assign category_slug = dataset[0] %}
  {% assign category_papers = dataset[1] %}
  {% assign category_name = category_slug | replace: '_', ' ' | capitalize %}

  <div class="category-section" id="{{ category_slug }}">
    <h2>{{ category_name }}</h2>
    <ul style="list-style-type: none; padding-left: 0;">
    
    {% assign sorted_papers = category_papers | sort: "year" | reverse %}
    
    {% for paper in sorted_papers %}
      <li class="paper-item" style="margin-bottom: 15px; padding: 15px; border: 1px solid #eaeaea; border-radius: 6px; background-color: #fcfcfc;">
        <strong style="font-size: 1.1em;">
          <a href="{{ paper.url }}" target="_blank" class="paper-title">{{ paper.title }}</a>
        </strong> ({{ paper.year }})<br>
        
        {% if paper.notes %}
          <div class="paper-notes" style="margin-top: 8px; font-size: 0.95em; color: #555;">
            <strong>Notes:</strong> {{ paper.notes }}
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
// --- Search Functionality ---
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

    // Hide empty categories when filtering
    for (let j = 0; j < categorySections.length; j++) {
        let visibleItems = categorySections[j].querySelectorAll('.paper-item:not([style*="display: none"])');
        if (visibleItems.length === 0) {
            categorySections[j].style.display = "none";
        } else {
            categorySections[j].style.display = "";
        }
    }
}

// --- Back to Top Functionality ---
let topButton = document.getElementById("backToTopBtn");

// When the user scrolls down 300px from the top of the document, show the button
window.onscroll = function() {
  if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
    topButton.style.display = "block";
  } else {
    topButton.style.display = "none";
  }
};

// When the user clicks on the button, scroll to the top of the document
function scrollToTop() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}
</script>