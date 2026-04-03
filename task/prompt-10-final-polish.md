# Prompt 10 — Final Polish, Deployment Prep & Project Report

## Your Task

You are a senior Django developer and technical writer. My **Topiq** project is fully built and tested. Now do the **final polish** — production settings, security hardening, performance improvements, and write the complete **project report** for university submission.

---

## Part 1 — Final `settings.py` Hardening

Rewrite the complete `topiq/settings.py` with production-safe settings:

### Security Settings
```python
# Read from .env
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Security headers (for production)
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### Session Settings
```python
SESSION_COOKIE_AGE = 86400 * 7   # 7 days
SESSION_SAVE_EVERY_REQUEST = False
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
```

### Static Files (Production)
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'website' / 'static']
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
```

### Logging Configuration
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'topiq.log',
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'website': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'ERROR',
            'propagate': False,
        },
    },
}
```

---

## Part 2 — Performance Improvements

### 1. Add DB Query Optimization in `recommender.py`

Replace slow queries with optimized versions:

```python
# SLOW — N+1 query problem:
topics = Topic.objects.all()
for topic in topics:
    print(topic.subject.name)   # hits DB each time

# FAST — use select_related:
topics = Topic.objects.select_related('subject__semester').filter(is_active=True)
```

Show where to apply `select_related()` and `prefetch_related()` in all views and recommender functions.

### 2. Add Simple Caching to `search_results` View

```python
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# Cache search results for 10 minutes per query
def search_results(request):
    query = request.GET.get('q', '').strip()
    cache_key = f'search_{query.lower().replace(" ", "_")}'
    cached_result = cache.get(cache_key)
    
    if cached_result:
        result = cached_result
    else:
        result = search_topics(query)
        cache.set(cache_key, result, 600)  # 10 minutes
```

Add `CACHES` configuration to settings.py using local memory cache (no Redis needed):
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'topiq-cache',
    }
}
```

### 3. Add `select_related` in Views

Show the exact query optimizations for the `search_results` view context building.

---

## Part 3 — Final `requirements.txt`

Write the complete, exact `requirements.txt`:

```
Django==4.2.x
python-dotenv==1.0.x
scikit-learn==1.4.x
numpy==1.26.x
requests==2.31.x
Pillow==10.x.x
```

Also write the full setup commands:
```bash
python -m venv myenv
source myenv/bin/activate          # Linux/Mac
# OR: myenv\Scripts\activate       # Windows
pip install -r requirements.txt
```

---

## Part 4 — Final `.env.example` File

```env
# Django Settings
SECRET_KEY=your-secret-key-here-generate-a-new-one
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Anthropic AI API Key
# Get your key from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx

# Optional Settings
DATABASE_URL=sqlite:///db.sqlite3
```

---

## Part 5 — Final `run.sh` Script

Write the complete production-ready `run.sh`:

```bash
#!/bin/bash

echo "🚀 Starting Topiq..."

# Activate virtual environment
source myenv/bin/activate

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found! Copy .env.example to .env and fill in your values."
    exit 1
fi

# Install/update dependencies
pip install -r requirements.txt -q

# Run migrations
echo "📦 Running migrations..."
python manage.py migrate --run-syncdb

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput -v 0

# Seed data if DB is empty
echo "🌱 Checking seed data..."
python manage.py seed_data

# Create logs directory
mkdir -p logs

# Start server
echo "✅ Server starting at http://127.0.0.1:8000/"
python manage.py runserver 0.0.0.0:8000
```

---

## Part 6 — University Project Report

Write the **complete project report** in Markdown format suitable for university final year submission. This is the most important part of this prompt.

### Report Structure:

---

**COVER PAGE**
```
Project Title: Topiq — Smart Learning Resource Recommendation System
Submitted by: [Your Name]
Student ID: [Your ID]
Department: Computer Science & Engineering
University: [University Name]
Supervisor: [Supervisor Name]
Submission Date: [Date]
```

---

**ABSTRACT** (250–300 words)

Write a professional abstract covering:
- Problem being solved
- Approach taken
- Technologies used
- Key results/achievements
- Conclusion

---

**CHAPTER 1 — INTRODUCTION**

Sections:
1.1 Background  
1.2 Problem Statement (2 paragraphs)  
1.3 Objectives (numbered list, 6 objectives)  
1.4 Scope of the Project  
1.5 Report Organization  

---

**CHAPTER 2 — LITERATURE REVIEW**

Write about:
- Existing learning management systems (Moodle, Coursera, Khan Academy) — what they do and what they lack
- Resource recommendation systems in education — research overview
- Why a topic-based, lightweight system is needed
- Gap this project fills

Minimum 4 paragraphs, cite general concepts (no specific papers needed).

---

**CHAPTER 3 — SYSTEM DESIGN & METHODOLOGY**

Sections:  
3.1 System Architecture (describe the flow: User → Browser → Django → Recommender → DB → Response)  
3.2 Technology Stack (table: Technology | Purpose | Version)  
3.3 Database Design (describe all 6 models with their relationships)  
3.4 ML Recommendation Engine:
  - TF-IDF explanation
  - Scoring formula: `score = rating × 0.4 + normalized_view_count × 0.3 + feedback_score × 0.3`
  - Why these weights were chosen
  - Feedback loop explanation  
3.5 System Flow Diagrams (ASCII text diagrams for: Search Flow, Feedback Loop)

---

**CHAPTER 4 — IMPLEMENTATION**

Sections:  
4.1 Development Environment Setup  
4.2 Backend Implementation (Django models, views, recommender)  
4.3 Frontend Implementation (templates, CSS, JavaScript)  
4.4 AI Chat Integration (Claude API)  
4.5 Database Seeding  

Include key code snippets with explanations (scoring formula, TF-IDF search, AJAX feedback).

---

**CHAPTER 5 — TESTING & RESULTS**

Sections:  
5.1 Testing Methodology (unit tests, integration tests, manual testing)  
5.2 Test Cases Table:

| Test ID | Test Case | Expected Result | Actual Result | Status |
|---------|-----------|----------------|---------------|--------|
| TC01 | Search "deadlock" | 3 videos + 3 readings shown | 3 videos + 3 readings | ✅ Pass |
| TC02 | Search empty string | Redirect with error | Redirected | ✅ Pass |
| ... | ... | ... | ... | ... |

Add 10 test cases total.  

5.3 Performance Observations  
5.4 Known Limitations  

---

**CHAPTER 6 — CONCLUSION & FUTURE WORK**

Sections:  
6.1 Conclusion (3–4 paragraphs summarizing what was achieved)  
6.2 Future Work:
  - Collaborative filtering for personalized recommendations
  - User accounts with CGPA-based content personalization
  - Mobile app version
  - Admin dashboard with analytics
  - Integration with university LMS
  - Multilingual support (Bengali + English)

---

**REFERENCES**

List 8–10 references:
- Django documentation
- Scikit-learn documentation
- Anthropic Claude API documentation
- Operating System textbook (Silberschatz)
- Research papers on recommendation systems
- TF-IDF / NLP references

---

## Output Requirements

- All 6 parts written completely — no shortcuts
- Project report: professional academic language, complete chapters
- Code snippets inside report properly formatted in code blocks
- Settings.py must be copy-paste ready with all new additions
- run.sh must be executable and work on Linux/Mac
- requirements.txt must have realistic version numbers
