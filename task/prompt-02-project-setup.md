# Prompt 02 — Django Project Setup & Configuration

## Your Task

You are a senior Django developer. I already have a Django project created. My current project structure is:

```
topiq/                     ← root folder
├── db.sqlite3
├── manage.py
├── requirements.txt
├── run.sh
├── myenv/                 ← virtual environment
├── documentation/
├── task/
├── topiq/                 ← Django settings folder
└── website/               ← Main Django app (already created)
```

Now I need you to **set up and configure the entire project from scratch** — settings, static files, templates, environment variables, and URL routing. Give me every file with full, complete, copy-paste ready code. Do not skip any file. Do not give partial code.

---

## Step 1 — Install Dependencies

Create the complete `requirements.txt` file with exact versions for:

```
Django
python-dotenv
scikit-learn
numpy
requests
Pillow
```

Also write the exact pip install command.

---

## Step 2 — Environment Variables

Create a `.env` file template with these variables:

```
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
ANTHROPIC_API_KEY=
DATABASE_URL=
```

Explain what each variable does and how to generate `SECRET_KEY`.

---

## Step 3 — `topiq/settings.py` — Full Configuration

Write the complete `settings.py` file that includes:

- Reads `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` from `.env` using `python-dotenv`
- `INSTALLED_APPS` includes `website`
- `TEMPLATES` configured to find templates inside `website/templates/`
- `STATICFILES_DIRS` points to `website/static/`
- `STATIC_URL = '/static/'`
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- `MEDIA_URL` and `MEDIA_ROOT` configured
- `DATABASES` using SQLite (db.sqlite3)
- `LOGIN_URL`, `LOGIN_REDIRECT_URL` set
- `SESSION_ENGINE` using database sessions
- All other default settings kept intact

---

## Step 4 — `topiq/urls.py` — Main URL Config

Write the complete `topiq/urls.py` that:
- Includes `website.urls`
- Serves static and media files in development
- Has `admin/` path

---

## Step 5 — `website/urls.py` — App URL Config

Create `website/urls.py` with placeholder URL patterns for:

```python
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_results, name='search_results'),
    path('api/search/', views.api_search, name='api_search'),
    path('api/chat/', views.ai_chat, name='ai_chat'),
    path('bookmark/', views.bookmark_topic, name='bookmark_topic'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
]
```

Also create a temporary `website/views.py` with placeholder views (just `HttpResponse("OK")`) so the URLs don't break.

---

## Step 6 — Static & Template Folder Structure

Write the exact terminal commands to create this structure:

```
website/
├── templates/
│   └── website/
│       ├── base.html        ← create empty file
│       ├── index.html       ← already exists
│       └── results.html     ← create empty file
└── static/
    └── website/
        ├── css/
        │   └── style.css    ← create empty file
        └── js/
            └── main.js      ← create empty file
```

---

## Step 7 — `website/templates/website/base.html`

Write the complete `base.html` that:
- Loads `{% load static %}`
- Has `<head>` with meta tags, title block, Google Fonts (Sora + DM Serif Display), CSS link
- Has `{% block content %}{% endblock %}`
- Has JavaScript link at bottom
- Uses `{% block title %}Topiq{% endblock %}` pattern

---

## Step 8 — `run.sh` Shell Script

Write the complete `run.sh` script that:
- Activates the `myenv` virtual environment
- Runs `python manage.py migrate`
- Runs `python manage.py collectstatic --noinput`
- Starts the server on `0.0.0.0:8000`

---

## Step 9 — `website/management/` Setup

Write the terminal commands to create:

```
website/
└── management/
    ├── __init__.py
    └── commands/
        ├── __init__.py
        └── seed_data.py     ← empty for now
```

---

## Step 10 — Verify Everything Works

Give me the exact commands to:
1. Activate virtual environment
2. Install requirements
3. Run migrations
4. Create superuser
5. Start server
6. Verify at `http://127.0.0.1:8000/`

Also list the **5 most common Django setup errors** and how to fix each one:
- ModuleNotFoundError
- TemplateDoesNotExist
- Static files not loading
- ALLOWED_HOSTS error
- SECRET_KEY not found

---

## Output Requirements

- Every file must be **complete** — no `# ... rest of code` shortcuts
- All code must be **copy-paste ready**
- Use proper Python/Django best practices
- Add comments explaining important lines
- At the end, show the expected terminal output when the server starts successfully
