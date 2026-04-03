# Prompt 06 — HTML Templates (`base.html`, `index.html`, `results.html`)

## Your Task

You are a senior frontend developer and Django template expert. I am building **Topiq** — a Smart Learning Resource Recommendation System for university students. Now write the **complete HTML templates** for all 3 pages. Every template must be fully working, beautifully designed, and use Django template tags properly.

---

## Design Reference

The existing design uses:
- **Fonts:** Sora (body) + DM Serif Display (headings) from Google Fonts
- **Theme:** Dark background, gradient accents, clean cards
- **Colors:**
  - Background: `#0a0a0f`
  - Card background: `#111118`
  - Border: `rgba(255,255,255,0.08)`
  - Primary gradient: `linear-gradient(135deg, #6366f1, #8b5cf6)`
  - Red accent: `#DC2626`
  - Blue accent: `#1E88E5`
  - Green accent: `#059669`
  - Purple accent: `#7C3AED`
  - Text: `#e8e8f0` (primary), `#888899` (muted)

---

## Template 1 — `website/templates/website/base.html`

Write the complete base template:

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- meta tags, title block, Google Fonts -->
  <!-- link to style.css -->
  {% block extra_css %}{% endblock %}
</head>
<body>
  <!-- HEADER: include a reusable header with logo + search bar -->
  {% block header %}
    <!-- include the header partial -->
  {% endblock %}
  
  {% block content %}{% endblock %}
  
  <!-- AI CHAT PANEL (always present on all pages) -->
  {% block chat_panel %}
    <!-- full chat panel HTML here -->
  {% endblock %}
  
  <script src="{% static 'website/js/main.js' %}"></script>
  {% block extra_js %}{% endblock %}
</body>
</html>
```

The base.html must include:
1. Full `<head>` with all meta tags, Open Graph tags, favicon placeholder
2. `{% block title %}Topiq{% endblock %}` inside `<title>`
3. Google Fonts link (Sora + DM Serif Display)
4. `{% static %}` link to `style.css`
5. Header HTML (logo + search bar that submits GET to `{% url 'website:search_results' %}?q=...`)
6. The complete AI Chat Panel HTML (overlay + panel + messages area + input row)
7. Footer with "Topiq © 2025 — Smart Resource Finder for University Students"
8. JS script tag at bottom

The header search bar must:
- Use `<form method="GET" action="{% url 'website:search_results' %}">`
- Input name must be `q`
- On the results page, pre-fill with `{{ query }}` value

---

## Template 2 — `website/templates/website/index.html`

Write the complete homepage template:

```html
{% extends 'website/base.html' %}
{% load static %}

{% block title %}Topiq — Smart Study Resource Finder{% endblock %}

{% block content %}
  <!-- HERO SECTION -->
  <!-- STATS / FEATURE BADGES -->
  <!-- SEARCH SECTION (large centered search) -->
  <!-- SEMESTER FILTER BUTTONS -->
  <!-- RECENT SEARCHES -->
  <!-- HOW IT WORKS SECTION -->
  <!-- FEATURES SECTION -->
{% endblock %}
```

Each section in detail:

### Hero Section
```html
<div class="hero">
  <div class="hero-badge">★ Smart Resource Finder for University Students</div>
  <h1>Find the <em>Best Resources</em><br>for Any Topic, Instantly</h1>
  <p>No more searching across YouTube, blogs & PDFs separately...</p>
</div>
```

### Large Search Bar
- `<form method="GET" action="{% url 'website:search_results' %}">`
- Big input with name `q`
- Placeholder: "Search your study topic… e.g. Deadlock, Binary Tree"
- Submit button

### Semester Filter
```html
{% if semesters %}
<div class="semester-filter">
  <span>Filter by Semester:</span>
  {% for semester in semesters %}
    <a href="{% url 'website:search_results' %}?semester={{ semester.id }}" class="semester-chip">
      {{ semester.name }}
    </a>
  {% endfor %}
</div>
{% endif %}
```

### Recent Searches
```html
{% if recent_searches %}
<div class="recent-searches">
  <span>Recent:</span>
  {% for search in recent_searches %}
    <a href="{% url 'website:search_results' %}?q={{ search }}" class="recent-chip">{{ search }}</a>
  {% endfor %}
</div>
{% endif %}
```

### Stats Bar
```html
<div class="stats-bar">
  <div class="stat-chip">📚 <strong>{{ total_resources }}+</strong> Resources Available</div>
  <div class="stat-chip">🎯 Topic-Based Smart Search</div>
  <div class="stat-chip">🤖 AI Study Assistant</div>
</div>
```

### How It Works Section
3 steps with icons:
1. "Search a Topic" → Enter any university topic name
2. "Get Top 3 Resources" → Videos + Articles instantly ranked
3. "Learn Efficiently" → No overload, just the best content

---

## Template 3 — `website/templates/website/results.html`

Write the complete results page template:

```html
{% extends 'website/base.html' %}
{% load static %}

{% block title %}{{ query }} – Topiq Results{% endblock %}

{% block content %}
  <!-- Case 1: No results found -->
  {% if no_results %}
    <!-- NO RESULTS section -->
  {% else %}
    <!-- STATS BAR -->
    <!-- MAIN RESULTS GRID (2 columns) -->
    <!-- SIMILAR TOPICS -->
  {% endif %}
{% endblock %}
```

### No Results State
```html
{% if no_results %}
<div class="no-results">
  <div class="no-results-icon">🔍</div>
  <h2>No resources found for "{{ query }}"</h2>
  <p>Try a different search term or browse by semester below.</p>
  <!-- list all semesters as quick links -->
  <!-- search form to try again -->
</div>
{% endif %}
```

### Stats Bar (dynamic)
```html
<div class="stats-bar">
  <div class="stat-chip">
    <span class="dot"></span> 
    Showing results for: <strong>{{ query }}</strong>
  </div>
  <div class="stat-chip">📚 <strong>{{ total_resources }}</strong> resources found</div>
  <div class="stat-chip">⏱ Avg. study time: <strong>{{ avg_study_time }}</strong></div>
  {% if semester_name %}
    <div class="stat-chip">📌 Semester: <strong>{{ semester_name }}</strong></div>
  {% endif %}
</div>
```

### Video Results Section
```html
{% if videos %}
<div class="section-header">
  <!-- YouTube icon + "Top 3 Video Suggestions" + count badge -->
</div>

{% for video in videos %}
<div class="video-card">
  <div class="video-thumb">
    {% if video.thumbnail_url %}
      <img src="{{ video.thumbnail_url }}" alt="{{ video.title }}">
    {% endif %}
    <span class="diff-badge {{ video.difficulty_level }}">{{ video.get_difficulty_level_display }}</span>
    <div class="play-btn">▶</div>
    <span class="duration-badge">{{ video.duration }}</span>
  </div>
  <div class="video-body">
    <div class="video-title">{{ video.title }}</div>
    <div class="video-desc">{{ video.description }}</div>
    
    <!-- WHY THIS RESOURCE badge -->
    {% if video.student_helpful_count > 0 %}
    <div class="why-badge">
      👍 {{ video.student_helpful_count }} students found this helpful
    </div>
    {% endif %}
    
    <!-- FEEDBACK BUTTONS -->
    <div class="feedback-row">
      <button class="feedback-btn helpful" 
              data-resource-type="video" 
              data-resource-id="{{ video.id }}"
              data-topic-id="{{ matched_topic.id }}">
        👍 Helpful
      </button>
      <button class="feedback-btn not-helpful"
              data-resource-type="video"
              data-resource-id="{{ video.id }}"
              data-topic-id="{{ matched_topic.id }}">
        👎 Not Helpful
      </button>
      <button class="bookmark-btn"
              data-topic-id="{{ matched_topic.id }}">
        {% if matched_topic.id in bookmarked_topics %}⭐{% else %}☆{% endif %} Save Topic
      </button>
    </div>
    
    <a href="{{ video.youtube_url }}" class="yt-btn" target="_blank" rel="noopener">
      ▶ Open on YouTube
    </a>
  </div>
</div>
{% endfor %}
{% endif %}
```

### Reading Results Section
```html
{% if readings %}
<div class="section-header">
  <!-- Article icon + "Articles & Blogs" + count badge -->
</div>

{% for reading in readings %}
<div class="article-card">
  <div class="article-icon {{ reading.resource_type }}">
    <!-- icon based on type -->
  </div>
  <div class="article-content">
    <div class="article-type type-{{ reading.resource_type }}">
      {{ reading.get_resource_type_display }}
    </div>
    <div class="article-title">{{ reading.title }}</div>
    <div class="article-desc">{{ reading.description }}</div>
    
    {% if reading.source_name %}
    <div class="source-badge">📌 Source: {{ reading.source_name }}</div>
    {% endif %}
    
    <!-- FEEDBACK BUTTONS same pattern as videos -->
    
    <a href="{{ reading.url }}" class="read-link" target="_blank" rel="noopener">
      Read Article →
    </a>
  </div>
</div>
{% endfor %}
{% endif %}
```

### Similar Topics Section
```html
{% if similar_topics %}
<div class="similar-topics">
  <h3>📌 Related Topics You Might Also Study</h3>
  <div class="topic-chips">
    {% for topic in similar_topics %}
    <a href="{% url 'website:search_results' %}?q={{ topic.name }}" class="topic-chip">
      {{ topic.name }}
    </a>
    {% endfor %}
  </div>
</div>
{% endif %}
```

---

## Django Template Tags Required

Make sure to use:
- `{% url 'website:search_results' %}` — all internal links
- `{% static '...' %}` — all static files
- `{{ variable }}` and `{{ variable|default:"—" }}` — data display
- `{% if %}` / `{% for %}` — all conditionals and loops
- `{% load static %}` — at top of every template
- `{{ video.get_difficulty_level_display }}` — for choice field display names
- `{% csrf_token %}` — inside all forms

---

## Output Requirements

- 3 complete template files
- Every Django tag correct
- All variables match what views.py sends in context
- No broken template syntax
- Mobile responsive meta viewport set in base.html
- All URLs use `{% url %}` tag — no hardcoded paths
