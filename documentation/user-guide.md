# Topiq User Guide

## 1. What This Project Does

Topiq is a Django-based study resource recommendation system for university students.

A student can:

- Search an academic topic like `Deadlock`, `Binary Tree`, or `Normalization`
- Get the top video suggestions
- Get the top reading materials
- Mark resources as helpful or not helpful
- Save topics in session bookmarks
- Ask academic questions using the AI chat feature

## 2. Main Technologies

- Python
- Django
- SQLite
- scikit-learn TF-IDF
- HTML, CSS, JavaScript
- Anthropic API for AI chat

## 3. How To Run The Project

### Option A: Run with script

```bash
chmod +x run.sh
./run.sh
```

The app starts at:

```text
http://127.0.0.1:8090/
```

### Option B: Run manually

```bash
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py seed_data
python manage.py runserver 0.0.0.0:8090
```

## 4. Environment File

Create a `.env` file from `.env.example`.

Important values:

- `SECRET_KEY`
- `DEBUG=True` for local development
- `AI_PROVIDER=groq` for the free demo setup
- `GROQ_API_KEY` if you want AI chat to work with Groq
- `ANTHROPIC_API_KEY` only if you want Anthropic as backup

If no valid AI provider key is present, the main search still works, but AI chat will show a fallback message.

## 5. How To Use The System

### Search

1. Open the homepage
2. Enter a topic name
3. Optionally select a semester
4. Press search

### Results Page

You will see:

- Recommended videos
- Recommended articles, blogs, and notes
- Average study time
- Subject and semester context
- Related topics

### Feedback

Students can click:

- `Helpful`
- `Not Helpful`
- `Save Topic`

This feedback is stored in the database and affects recommendation ranking.

## 6. How To Seed Or Refresh The Database

This project does not train a deep learning model. Instead, it uses:

- TF-IDF topic matching
- Ranking scores from rating, views, and student feedback

So when someone asks, "How do you train the database?", the correct answer is:

This project mainly seeds and updates structured academic data. It does not train a neural network model. It improves results through topic indexing plus feedback-driven ranking.

### Seed data

```bash
python manage.py seed_data
```

### Seed from scratch

```bash
python manage.py seed_data --flush
```

### Demo-only seed

```bash
python manage.py seed_data --flush --demo
```

Use `--flush` when you want to refresh all seeded records, including YouTube search links and ranking values.

## 7. How Recommendation Works

1. User enters a topic
2. Query is normalized
3. TF-IDF compares the query with topic name, tags, keywords, and description
4. Best matching topic is selected
5. Top 3 videos and top 3 readings are returned by `ml_score`

### ML score formula

The system uses a weighted score based on:

- Rating
- View count
- Helpful vs not helpful feedback

This makes the project easy to explain in an academic presentation.

## 8. Admin Usage

Open:

```text
http://127.0.0.1:8090/admin/
```

You can manage:

- Semesters
- Subjects
- Topics
- Video resources
- Reading resources
- Student interactions

If needed, create an admin user:

```bash
python manage.py createsuperuser
```

## 9. API Endpoints

- `/` home page
- `/search/?q=deadlock` search results
- `/api/search/?q=deadlock` JSON search endpoint
- `/api/chat/` AI academic chat
- `/feedback/` feedback submission
- `/bookmark/` topic bookmark

## 10. Common Problems And Fixes

### YouTube link not opening correct video

Seeded demo videos now use YouTube search links, not fake video IDs.

Run:

```bash
python manage.py seed_data --flush
```

### AI chat not working

Reason:

- `GROQ_API_KEY` not set
- or the selected provider key is invalid

Fix:

- Add the correct API key in `.env`
- For free/demo use, prefer Groq with `AI_PROVIDER=groq`

### No results found

Try:

- A simpler keyword
- Exact topic name
- Searching without semester filter

### Static CSS not loading

Run:

```bash
python manage.py collectstatic --noinput
```

## 11. Suggested Demo Flow

Use this order in a live demo:

1. Search `Deadlock`
2. Show recommended videos and readings
3. Click `Helpful`
4. Save the topic
5. Ask AI chat: `Explain deadlock with example`
6. Show admin panel or database records if needed

## 12. Short Explanation For Teacher

Topiq is an academic resource recommendation platform. It takes a student topic query, matches it with stored curriculum topics using TF-IDF, and returns the best video and reading resources ranked by a scoring formula. The system also improves ranking using student feedback collected from real usage.
