# Prompt 01 — Full Project Documentation

## Your Task

You are a senior software engineer and technical writer. I am building a Django web application called **Topiq** — a Smart Topic-Based Learning Resource Recommendation System for university students.

Read everything below carefully and generate a **complete, professional project documentation** in Markdown format inside documentation folder. This documentation will be saved as `README.md` and also used as the official project report reference.

---

## Project Overview

**Project Name:** Topiq  
**Type:** Final Year University Project (Web Application)  
**Tech Stack:** Python, Django, SQLite, Scikit-learn (TF-IDF), HTML/CSS/JS, Anthropic Claude API  
**App Name (Django):** `website`  
**Project Folder Name:** `topiq`

---

## Problem Statement

University students struggle to find high-quality, relevant learning resources for specific academic topics. They have to search YouTube, blogs, and PDF repositories separately, which is time-consuming and results in information overload. There is no centralized system that provides semester-wise, topic-based, and quality-filtered learning resource recommendations tailored for students.

---

## Solution

Topiq solves this by allowing students to:
- Search any academic topic (e.g., "Operating System – Deadlock")
- Get **Top 3 Video Resources** (YouTube) ranked by quality
- Get **Top 3 Reading Resources** (PDF, Blog, Notes) ranked by relevance
- Use an **AI Chat Assistant** for academic questions (Claude API)
- **Bookmark** topics for later study
- **Give feedback** (Helpful / Not Helpful) to improve recommendations

---

## Core Features to Document

1. **Smart Search** — Topic-based search with semester filter
2. **Video Recommendations** — Top 3 YouTube videos with difficulty level (Beginner / Intermediate / Advanced), duration, description
3. **Reading Recommendations** — Top 3 resources: PDF Textbook, Blog Article, Study Notes
4. **ML Ranking System** — Resources ranked using a scoring formula:  
   `score = rating × 0.4 + normalized_view_count × 0.3 + student_feedback_score × 0.3`
5. **TF-IDF Search Intelligence** — Similar topic names return same results (e.g., "Binary Tree" = "Tree in DS")
6. **AI Chat Assistant** — Powered by Claude API, university-level academic questions only
7. **Bookmark System** — Save topics for later
8. **Feedback System** — Helpful / Not Helpful ratings improve future recommendations
9. **Similar Topic Suggestions** — After viewing a topic, related topics are suggested
10. **Semester-wise Filter** — Same topic can have easy vs advanced versions per semester

---

## Django Project Structure to Document

```
topiq/                          ← Django project root
├── manage.py
├── db.sqlite3
├── requirements.txt
├── .env                        ← API keys, SECRET_KEY
├── run.sh                      ← Shell script to run server
├── README.md
├── documentation/              ← Project docs folder
│
├── topiq/                      ← Django project settings folder
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── website/                    ← Main Django app
    ├── models.py               ← Database models
    ├── views.py                ← All views/logic
    ├── urls.py                 ← URL routing
    ├── admin.py                ← Admin panel setup
    ├── recommender.py          ← ML recommendation engine
    ├── forms.py                ← Django forms
    │
    ├── templates/
    │   └── website/
    │       ├── base.html
    │       ├── index.html      ← Homepage with search
    │       └── results.html    ← Search results page
    │
    ├── static/
    │   └── website/
    │       ├── css/
    │       │   └── style.css
    │       └── js/
    │           └── main.js
    │
    └── management/
        └── commands/
            └── seed_data.py    ← Populate sample data
```

---

## Database Models to Document

Document each model with field names, types, and purpose:

1. `Semester` — id, name (e.g., "5th Semester"), is_active
2. `Subject` — id, name, semester (FK), code, description
3. `Topic` — id, name, subject (FK), slug, description, is_active
4. `VideoResource` — id, topic (FK), title, description, youtube_url, thumbnail_url, duration, difficulty_level (choices: Beginner/Intermediate/Advanced), view_count, rating (0–5), student_feedback_count, is_active, created_at
5. `ReadingResource` — id, topic (FK), title, description, url, resource_type (choices: PDF/Blog/Notes), rating, view_count, student_feedback_count, is_active, created_at
6. `StudentInteraction` — id, session_key, topic (FK), resource_type, resource_id, interaction_type (bookmark/helpful/not_helpful), created_at

---

## ML / Recommendation Engine to Document

Explain in the documentation:
- Why ML is used here
- How TF-IDF works for topic name matching
- The scoring formula with explanation of each weight
- How feedback improves future recommendations (feedback loop)
- Future scope: Collaborative filtering, personalization by CGPA

---

## API & Views to Document

| URL | View | Method | Description |
|-----|------|--------|-------------|
| `/` | `index` | GET | Homepage |
| `/search/` | `search_results` | GET | Topic search results |
| `/api/search/` | `api_search` | GET | JSON search for AJAX |
| `/api/chat/` | `ai_chat` | POST | AI assistant response |
| `/bookmark/` | `bookmark_topic` | POST | Save topic |
| `/feedback/` | `submit_feedback` | POST | Helpful/Not Helpful |

---

## What the Documentation Must Include

Generate the following sections in Markdown:

1. **Project Title & Badge Line** (Project name, tech stack badges)
2. **Table of Contents**
3. **Problem Statement** (formal, 1 paragraph)
4. **Project Objectives** (5–7 bullet points)
5. **System Architecture Diagram** (text-based ASCII diagram showing Request → Django → Recommender → DB → Response)
6. **Tech Stack Table** (Tool | Purpose | Version)
7. **Database Schema** (all 6 models with fields and types)
8. **ML Recommendation Engine Explanation** (how it works, formula, TF-IDF)
9. **Feature List** (all 10 features, explained)
10. **Project Folder Structure** (full tree)
11. **Setup & Installation Guide** (step by step: clone, virtualenv, install, migrate, seed, run)
12. **How to Use the Application** (student workflow step by step)
13. **API Endpoints Table**
14. **Future Scope** (5 ideas)
15. **Limitations** (3–4 honest limitations)
16. **Contributors / Author Section**

---

## Output Format

- Write in clean, professional **Markdown**
- Use headings (##, ###), tables, code blocks, bullet lists
- This will be submitted as a university final year project document
- Tone: professional but easy to understand
- Length: comprehensive, do not skip any section
