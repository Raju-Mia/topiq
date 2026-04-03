# Topiq — Smart Learning Resource Recommendation System

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=flat-square&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-TF--IDF-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![Claude API](https://img.shields.io/badge/Claude-AI%20Assistant-7C3AED?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> **A topic-based, ML-powered learning resource recommendation web application for university students — built with Django.**

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Project Objectives](#2-project-objectives)
3. [System Architecture](#3-system-architecture)
4. [Tech Stack](#4-tech-stack)
5. [Database Schema](#5-database-schema)
6. [ML Recommendation Engine](#6-ml-recommendation-engine)
7. [Features](#7-features)
8. [Project Structure](#8-project-structure)
9. [Setup & Installation](#9-setup--installation)
10. [How to Use](#10-how-to-use)
11. [API Endpoints](#11-api-endpoints)
12. [Future Scope](#12-future-scope)
13. [Limitations](#13-limitations)
14. [Author](#14-author)

---

## 1. Problem Statement

University students often struggle to find high-quality and relevant learning resources for specific academic topics. When preparing for exams or trying to understand a concept, a student must manually search across multiple platforms — YouTube for video lectures, Google for blog articles, and various repositories for PDF textbooks. This fragmented process is time-consuming, mentally exhausting, and frequently results in information overload where the student is presented with hundreds of low-quality, irrelevant, or inappropriately levelled results. Without a centralized, intelligent system, students waste valuable study time navigating content rather than learning it. **Topiq** addresses this gap by providing a single platform where a student can enter any academic topic and instantly receive the top three most effective video resources and top three reading resources, ranked by a machine learning scoring engine and refined continuously through student feedback.

---

## 2. Project Objectives

- **Centralize** learning resources from YouTube, blog platforms, and PDF repositories into a single searchable system.
- **Rank** resources intelligently using a machine learning scoring formula based on ratings, view counts, and student feedback.
- **Match** topic search queries intelligently using TF-IDF so that variations like *"Binary Tree"* and *"Tree in DS"* return the same results.
- **Filter** resources by semester and difficulty level (Beginner / Intermediate / Advanced) to match a student's current level.
- **Provide** an AI-powered study assistant (Claude API) that answers university-level academic questions in context.
- **Improve** over time through a student feedback loop — Helpful / Not Helpful ratings directly influence future recommendation scores.
- **Reduce** study friction so students spend more time learning and less time searching.

---

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        STUDENT (Browser)                        │
│                  Types topic: "OS – Deadlock"                   │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP GET /search/?q=deadlock
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DJANGO BACKEND                           │
│                                                                 │
│   urls.py  ──►  views.py (search_results)                       │
│                      │                                          │
│                      ▼                                          │
│            recommender.py                                       │
│            ┌──────────────────────────────┐                     │
│            │  1. Clean & normalize query  │                     │
│            │  2. Build TF-IDF corpus from │                     │
│            │     all Topic names + tags   │                     │
│            │  3. Compute cosine similarity│                     │
│            │  4. Find best matching Topic │                     │
│            │  5. Fetch top 3 VideoResource│                     │
│            │     ordered by ml_score      │                     │
│            │  6. Fetch top 3 Reading      │                     │
│            │     ordered by ml_score      │                     │
│            │  7. Return result dict       │                     │
│            └──────────────┬───────────────┘                     │
│                           │                                     │
│                           ▼                                     │
│                     SQLite Database                             │
│            (Semester, Subject, Topic,                           │
│             VideoResource, ReadingResource,                     │
│             StudentInteraction)                                 │
│                           │                                     │
│                           ▼                                     │
│              views.py builds context dict                       │
│              renders results.html template                      │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTML Response
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STUDENT SEES RESULTS                         │
│                                                                 │
│   ┌──────────────────────┐   ┌──────────────────────────────┐  │
│   │  📺 Top 3 Videos      │   │  📄 Top 3 Reading Resources  │  │
│   │  • Beginner video     │   │  • PDF Textbook              │  │
│   │  • Intermediate video │   │  • Blog Article              │  │
│   │  • Advanced video     │   │  • Study Notes               │  │
│   └──────────────────────┘   └──────────────────────────────┘  │
│                                                                 │
│   [👍 Helpful]  [👎 Not Helpful]  [☆ Bookmark]  [🤖 AI Chat]   │
└─────────────────────────────────────────────────────────────────┘
                               │
               Student clicks 👍 Helpful
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FEEDBACK LOOP                              │
│                                                                 │
│   POST /feedback/  ──►  StudentInteraction saved in DB          │
│                         resource.student_helpful_count++        │
│                         resource.calculate_ml_score()           │
│                         ml_score updated in DB                  │
│                         Next search → better ranked result      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Tech Stack

| Technology | Purpose | Version |
|---|---|---|
| **Python** | Core programming language | 3.11+ |
| **Django** | Web framework — views, models, URLs, templates | 4.2 |
| **SQLite** | Lightweight relational database | Built-in |
| **scikit-learn** | TF-IDF vectorizer + cosine similarity for topic matching | 1.4+ |
| **NumPy** | Numerical operations for ML scoring | 1.26+ |
| **Requests** | HTTP calls to Anthropic Claude API | 2.31+ |
| **python-dotenv** | Load environment variables from `.env` file | 1.0+ |
| **HTML5 / CSS3** | Frontend structure and styling | — |
| **Vanilla JavaScript** | AJAX calls, chat UI, feedback interactions | ES6+ |
| **Google Fonts** | Typography — Sora + DM Serif Display | — |
| **Anthropic Claude API** | AI study assistant (academic Q&A) | claude-3-haiku |
| **Django Admin** | Built-in admin panel for managing data | Built-in |

---

## 5. Database Schema

### 5.1 Entity Relationship Overview

```
Semester ──< Subject ──< Topic ──< VideoResource
                                └──< ReadingResource
                                └──< StudentInteraction
```

---

### 5.2 Model: `Semester`

Represents an academic semester (e.g., "5th Semester").

| Field | Type | Description |
|---|---|---|
| `id` | AutoField | Primary key |
| `name` | CharField(50) | e.g., "1st Semester", "5th Semester" |
| `order` | IntegerField | Sort order (1, 2, 3...) |
| `is_active` | BooleanField | Whether shown to students |
| `created_at` | DateTimeField | Auto timestamp |

---

### 5.3 Model: `Subject`

Represents a university subject within a semester.

| Field | Type | Description |
|---|---|---|
| `id` | AutoField | Primary key |
| `semester` | ForeignKey → Semester | Which semester this belongs to |
| `name` | CharField(100) | e.g., "Operating System" |
| `code` | CharField(20) | e.g., "CS301" (optional) |
| `description` | TextField | Brief subject description |
| `is_active` | BooleanField | Visibility toggle |
| `created_at` | DateTimeField | Auto timestamp |

---

### 5.4 Model: `Topic`

Represents a specific topic within a subject that students search for.

| Field | Type | Description |
|---|---|---|
| `id` | AutoField | Primary key |
| `subject` | ForeignKey → Subject | Parent subject |
| `name` | CharField(150) | e.g., "Deadlock" |
| `slug` | SlugField | Auto-generated URL-safe name |
| `description` | TextField | Topic description |
| `tags` | CharField(300) | Comma-separated keywords for ML matching |
| `search_keywords` | TextField | Extra synonyms for TF-IDF |
| `is_active` | BooleanField | Visibility toggle |
| `created_at` | DateTimeField | Auto timestamp |
| `updated_at` | DateTimeField | Auto update timestamp |

---

### 5.5 Model: `VideoResource`

Stores a YouTube video resource linked to a topic.

| Field | Type | Description |
|---|---|---|
| `id` | AutoField | Primary key |
| `topic` | ForeignKey → Topic | Parent topic |
| `title` | CharField(200) | Video title |
| `description` | TextField | What the video covers |
| `youtube_url` | URLField | Full YouTube URL |
| `youtube_video_id` | CharField(20) | Extracted video ID (auto) |
| `thumbnail_url` | URLField | Auto-generated from video ID |
| `duration` | CharField(10) | e.g., "18:42" |
| `duration_seconds` | IntegerField | For sorting by length |
| `difficulty_level` | CharField | `beginner` / `intermediate` / `advanced` |
| `view_count` | IntegerField | YouTube-style view count |
| `rating` | FloatField | 0.0 – 5.0 |
| `student_helpful_count` | IntegerField | Times marked helpful |
| `student_not_helpful_count` | IntegerField | Times marked not helpful |
| `ml_score` | FloatField | Pre-calculated recommendation score |
| `is_active` | BooleanField | Visibility toggle |
| `created_at` | DateTimeField | Auto timestamp |

---

### 5.6 Model: `ReadingResource`

Stores a reading resource (PDF, Blog, Notes) linked to a topic.

| Field | Type | Description |
|---|---|---|
| `id` | AutoField | Primary key |
| `topic` | ForeignKey → Topic | Parent topic |
| `title` | CharField(200) | Resource title |
| `description` | TextField | What the resource covers |
| `url` | URLField | Link to the resource |
| `resource_type` | CharField | `pdf` / `blog` / `notes` / `article` |
| `source_name` | CharField(100) | e.g., "GeeksForGeeks" (optional) |
| `rating` | FloatField | 0.0 – 5.0 |
| `view_count` | IntegerField | Popularity count |
| `student_helpful_count` | IntegerField | Times marked helpful |
| `student_not_helpful_count` | IntegerField | Times marked not helpful |
| `ml_score` | FloatField | Pre-calculated recommendation score |
| `is_active` | BooleanField | Visibility toggle |
| `created_at` | DateTimeField | Auto timestamp |

---

### 5.7 Model: `StudentInteraction`

Records every student action (bookmark, feedback, view) without requiring login — uses Django session key.

| Field | Type | Description |
|---|---|---|
| `id` | AutoField | Primary key |
| `session_key` | CharField(40) | Django session key (no login needed) |
| `topic` | ForeignKey → Topic | Which topic was interacted with |
| `resource_type` | CharField | `video` or `reading` |
| `resource_id` | IntegerField | ID of the specific resource |
| `interaction_type` | CharField | `bookmark` / `helpful` / `not_helpful` / `view` |
| `created_at` | DateTimeField | Auto timestamp |

> **Unique constraint:** `(session_key, topic, resource_type, resource_id, interaction_type)` — prevents duplicate interactions.

---

## 6. ML Recommendation Engine

### 6.1 Why Machine Learning?

Traditional search systems match exact keywords. A student typing *"dead lock"* or *"banker algo"* would get no results with simple string matching. The ML engine solves this by understanding the **semantic meaning** of a query and matching it against topic names, tags, and keywords — even when the phrasing is different.

---

### 6.2 How TF-IDF Search Works

**TF-IDF** (Term Frequency – Inverse Document Frequency) is a numerical statistic used to measure how important a word is in a document relative to a collection of documents.

**Step-by-step flow:**

```
1. CORPUS BUILDING
   ─────────────────────────────────────────────────────
   For each Topic in the database, build a document string:
   
   doc = "{topic.name} {subject.name} {topic.tags} {topic.search_keywords}"
   
   Example:
   "Deadlock Operating System deadlock coffman conditions 
    banker algorithm deadlock detection resource allocation"

2. VECTORIZATION
   ─────────────────────────────────────────────────────
   TfidfVectorizer().fit_transform(all_documents)
   → Converts all documents into a numerical matrix

3. QUERY MATCHING
   ─────────────────────────────────────────────────────
   query = "dead lock os"
   query_vector = vectorizer.transform([query])
   
   similarities = cosine_similarity(query_vector, corpus_matrix)
   → [0.82, 0.11, 0.03, 0.67, ...]  ← score per topic

4. RESULT SELECTION
   ─────────────────────────────────────────────────────
   Best match = Topic with highest similarity score
   Threshold = 0.15 (below this = no meaningful match)
```

**Why this handles synonyms:** Because TF-IDF works on word overlap across the full tag string, *"Tree in DS"* will still match the *"Binary Tree"* topic because both contain the word "tree" and the tags contain "data structure, DS, tree".

---

### 6.3 Resource Scoring Formula

Once the correct topic is found, all its resources are ranked using this formula:

```
ml_score = (rating × 0.4) + (normalized_view_count × 0.3) + (feedback_score × 0.3)
```

| Component | Weight | Description |
|---|---|---|
| `rating` | **0.4 (40%)** | Editorial quality rating (0–5). Highest weight because it reflects content quality. |
| `normalized_view_count` | **0.3 (30%)** | `view_count / 1,000,000`. Popularity signal — widely viewed resources are generally more trusted. |
| `feedback_score` | **0.3 (30%)** | `helpful / (helpful + not_helpful + 1)`. Direct signal from students on the platform. |

**Example calculation:**

```
Video: "Deadlock Full Explanation"
  rating             = 4.7
  view_count         = 245,000  → normalized = 0.245
  helpful            = 89, not_helpful = 4
  feedback_score     = 89 / (89 + 4 + 1) = 0.94

ml_score = (4.7 × 0.4) + (0.245 × 0.3) + (0.94 × 0.3)
         = 1.88 + 0.0735 + 0.282
         = 2.2355
```

Resources are then sorted by `ml_score` descending and the top 3 are returned.

---

### 6.4 Feedback Loop

```
Student clicks 👍 Helpful
        │
        ▼
StudentInteraction saved to DB
        │
        ▼
resource.student_helpful_count += 1
        │
        ▼
resource.calculate_ml_score() called
        │
        ▼
New ml_score saved to DB
        │
        ▼
Next student searching same topic
→ This resource now ranks higher
```

This creates a self-improving system — the more students use it, the better the recommendations become.

---

## 7. Features

### Feature 1 — Smart Topic Search
Students type any academic topic into the search bar. The system uses TF-IDF to find the best matching topic even with typos, abbreviations, or synonyms.

### Feature 2 — Top 3 Video Recommendations
For every topic, the system shows exactly 3 YouTube videos ranked by ML score. Each video card shows the title, description, duration, difficulty level badge (Beginner / Intermediate / Advanced), and a direct YouTube link.

### Feature 3 — Top 3 Reading Recommendations
Alongside videos, the system shows 3 reading resources — one PDF textbook chapter, one blog article, and one set of study notes — all ranked by ML score.

### Feature 4 — Difficulty Level Filtering
Every video is tagged with a difficulty level. Beginners see green badges, intermediate students see orange, and advanced learners see red — making it easy to pick the right resource at a glance.

### Feature 5 — AI Study Assistant
A chat panel powered by the Anthropic Claude API is available on every page. It answers only university-level academic questions, keeping the assistant focused on study help.

### Feature 6 — Bookmark Topics
Students can save any topic with a single click. Bookmarks are stored in the browser session — no login required. The star icon fills to confirm the save.

### Feature 7 — Helpful / Not Helpful Feedback
Every resource has thumbs up and thumbs down buttons. Feedback is saved to the database and directly updates the resource's ML score for future searches.

### Feature 8 — "Why This Resource?" Badge
Resources that have been marked helpful by many students display a badge like *"89 students found this helpful"* — adding social proof to the recommendation.

### Feature 9 — Similar Topic Suggestions
After viewing results for a topic, the system suggests 2–3 related topics from the same subject. For example, after *Deadlock*, it may suggest *Process Scheduling* and *Memory Management*.

### Feature 10 — Semester-wise Filter
The homepage shows all available semesters as filter chips. Clicking one filters search results to topics within that semester, making it easy for a 5th semester student to stay focused on their curriculum.

---

## 8. Project Structure

```
topiq/                              ← Django project root
│
├── manage.py                       ← Django management entry point
├── db.sqlite3                      ← SQLite database file
├── requirements.txt                ← Python dependencies
├── .env                            ← Environment variables (not committed)
├── .env.example                    ← Template for .env
├── run.sh                          ← Shell script to start server
├── README.md                       ← This file
│
├── documentation/                  ← Project documentation folder
│   ├── prompt-01-documentation.md
│   ├── prompt-02-project-setup.md
│   └── ...
│
├── topiq/                          ← Django project configuration
│   ├── __init__.py
│   ├── settings.py                 ← All settings (DB, static, templates)
│   ├── urls.py                     ← Root URL configuration
│   ├── wsgi.py                     ← WSGI entry point
│   └── asgi.py                     ← ASGI entry point
│
└── website/                        ← Main Django application
    ├── __init__.py
    ├── models.py                   ← Database models (6 models)
    ├── views.py                    ← All view functions (6 views)
    ├── urls.py                     ← App-level URL patterns
    ├── admin.py                    ← Django admin configuration
    ├── recommender.py              ← ML recommendation engine (TF-IDF)
    ├── forms.py                    ← SearchForm
    ├── tests.py                    ← Unit & integration tests
    │
    ├── templates/
    │   └── website/
    │       ├── base.html           ← Base layout with header, chat panel
    │       ├── index.html          ← Homepage with hero + search
    │       └── results.html        ← Search results (videos + readings)
    │
    ├── static/
    │   └── website/
    │       ├── css/
    │       │   └── style.css       ← All styles (dark theme)
    │       └── js/
    │           └── main.js         ← Chat, feedback, bookmarks (AJAX)
    │
    └── management/
        ├── __init__.py
        └── commands/
            ├── __init__.py
            └── seed_data.py        ← Populates DB with sample data
```

---

## 9. Setup & Installation

### Prerequisites

- Python 3.11 or higher
- pip
- Git

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/yourusername/topiq.git
cd topiq
```

---

### Step 2 — Create a Virtual Environment

```bash
# Create virtual environment
python -m venv myenv

# Activate on Linux / Mac
source myenv/bin/activate

# Activate on Windows
myenv\Scripts\activate
```

---

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt` contents:**
```
Django==4.2.11
python-dotenv==1.0.1
scikit-learn==1.4.2
numpy==1.26.4
requests==2.31.0
Pillow==10.3.0
```

---

### Step 4 — Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Open and edit .env
nano .env
```

Fill in your `.env` file:

```env
SECRET_KEY=django-insecure-your-secret-key-here-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

> **Get your Anthropic API key:** https://console.anthropic.com/

---

### Step 5 — Run Database Migrations

```bash
python manage.py makemigrations website
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, website
Running migrations:
  Applying website.0001_initial... OK
```

---

### Step 6 — Create Admin Superuser

```bash
python manage.py createsuperuser
```

Enter a username, email, and password when prompted.

---

### Step 7 — Seed Sample Data

```bash
python manage.py seed_data
```

Expected output:
```
✅ Seed data complete!
──────────────────────────────
Semesters created:    6
Subjects created:     8
Topics created:       20
Video resources:      60
Reading resources:    60
Total resources:      120
──────────────────────────────
```

---

### Step 8 — Start the Development Server

```bash
python manage.py runserver
```

Or use the provided shell script:

```bash
chmod +x run.sh
./run.sh
```

Open your browser at: **http://127.0.0.1:8000/**

---

## 10. How to Use

### Student Workflow

```
Step 1: Open http://127.0.0.1:8000/
        └── Homepage loads with search bar and semester filters

Step 2: Type a topic in the search bar
        └── Example: "Operating System Deadlock"
        └── Press Enter or click Search

Step 3: View results page
        ├── Left column: Top 3 YouTube Videos
        │     ├── Difficulty badge (Beginner / Intermediate / Advanced)
        │     ├── Duration (e.g., 18:42)
        │     ├── Description
        │     └── "Open on YouTube" button
        │
        └── Right column: Top 3 Reading Resources
              ├── Type badge (PDF / Blog / Notes)
              ├── Source name (e.g., GeeksForGeeks)
              ├── Description
              └── "Read Article" link

Step 4: Give feedback on resources
        └── Click 👍 Helpful or 👎 Not Helpful
        └── Toast notification confirms your feedback

Step 5: Bookmark the topic
        └── Click ☆ Save Topic
        └── Star fills → topic saved to your session

Step 6: Ask the AI Assistant
        └── Click the AI button (top right corner)
        └── Type your academic question
        └── e.g., "Explain the four Coffman conditions"
        └── AI replies with a clear, academic explanation

Step 7: Explore related topics
        └── Scroll down to "Related Topics You Might Also Study"
        └── Click any chip to search that topic
```

---

### Admin Workflow

```
1. Go to: http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Manage content:
   ├── Add / Edit Semesters
   ├── Add / Edit Subjects
   ├── Add / Edit Topics (with tags and search_keywords)
   ├── Add / Edit VideoResource entries
   ├── Add / Edit ReadingResource entries
   └── View StudentInteraction logs
```

---

## 11. API Endpoints

| Method | URL | View Function | Description | Auth Required |
|---|---|---|---|---|
| `GET` | `/` | `index` | Homepage with search bar and semesters | No |
| `GET` | `/search/?q=<query>` | `search_results` | Full results page for a topic search | No |
| `GET` | `/api/search/?q=<query>` | `api_search` | JSON response — for AJAX search | No |
| `POST` | `/api/chat/` | `ai_chat` | Send message to AI assistant | No |
| `POST` | `/bookmark/` | `bookmark_topic` | Bookmark or unbookmark a topic | No (session) |
| `POST` | `/feedback/` | `submit_feedback` | Submit helpful / not helpful rating | No (session) |

---

### Request / Response Examples

**`GET /api/search/?q=deadlock`**
```json
{
  "found": true,
  "query": "deadlock",
  "matched_topic_name": "Deadlock",
  "subject_name": "Operating System",
  "semester_name": "5th Semester",
  "videos": [
    {
      "id": 1,
      "title": "Deadlock in Operating System – Full Explanation",
      "youtube_url": "https://www.youtube.com/watch?v=...",
      "duration": "18:42",
      "difficulty_level": "beginner",
      "rating": 4.7
    }
  ],
  "readings": [
    {
      "id": 1,
      "title": "OS Concepts – Deadlock Chapter (Silberschatz)",
      "url": "https://...",
      "resource_type": "pdf",
      "source_name": "Silberschatz Textbook"
    }
  ],
  "total_resources": 6,
  "avg_study_time": "2.5 hrs"
}
```

**`POST /api/chat/`**
```json
// Request body
{
  "message": "What are the four conditions for deadlock?",
  "topic_context": "Deadlock"
}

// Response
{
  "reply": "Great question! The four necessary conditions for deadlock (Coffman Conditions) are:\n1. Mutual Exclusion\n2. Hold and Wait\n3. No Preemption\n4. Circular Wait",
  "status": "ok"
}
```

**`POST /feedback/`**
```json
// Request body
{
  "resource_type": "video",
  "resource_id": 1,
  "feedback_type": "helpful",
  "topic_id": 3
}

// Response
{
  "status": "ok",
  "feedback": "helpful",
  "resource_id": 1,
  "helpful_count": 90
}
```

---

## 12. Future Scope

1. **User Accounts & CGPA-Based Personalization**
   Students can register and log in. The system tracks their search history and adjusts recommendations based on their academic level — students with higher CGPAs receive more advanced resources automatically.

2. **Collaborative Filtering**
   Instead of relying only on a scoring formula, the system can use collaborative filtering to recommend resources based on what *similar students* found useful — similar to how Netflix or Spotify recommendations work.

3. **Mobile Application**
   A React Native or Flutter mobile app with push notifications to remind students about bookmarked topics before exams.

4. **Multilingual Support (Bengali + English)**
   Since this system targets Bangladeshi university students, adding Bengali language support for topic names, descriptions, and the AI assistant would make it significantly more accessible.

5. **Admin Analytics Dashboard**
   A real-time dashboard for administrators showing most searched topics, most helpful resources, student engagement stats, and recommendation accuracy metrics — helping institutions improve curriculum resources.

---

## 13. Limitations

1. **No Real-Time YouTube Data** — Video view counts and ratings are manually entered into the database rather than pulled from the YouTube Data API. This means the data can become outdated over time unless updated by an admin.

2. **Session-Based Only — No Persistent User Accounts** — Bookmarks and feedback are saved to the browser session. If a student clears cookies or switches devices, their saved data is lost. A full login system would solve this.

3. **TF-IDF Has Limits on Completely New Topics** — If a topic has very few or no tags defined in the database, the TF-IDF engine may fail to find it even when the topic exists. Quality of results depends on how well topics are tagged by the admin.

4. **AI Assistant Requires Internet + Paid API** — The Claude API requires an active internet connection and an API key from Anthropic. If the key is missing or the API is down, the chat assistant falls back to a generic error message rather than a local fallback model.

---

## 14. Author

**Project:** Topiq — Smart Learning Resource Recommendation System  
**Type:** Final Year University Project  
**Department:** Computer Science & Engineering

---

```
Built with ❤️ to help university students study smarter, not harder.
```

---

*Last updated: 2025*
