# Prompt 03 — Database Models (`models.py`)

## Your Task

You are a senior Django developer building a project called **Topiq** — a Smart Learning Resource Recommendation System for university students.

Write the **complete, production-ready `website/models.py`** file with all database models. Every model must be fully defined with all fields, Meta classes, `__str__` methods, and helper methods. Do not give partial code. Every line must be copy-paste ready.

---

## Project Context

- Framework: Django with SQLite
- App name: `website`
- Students search topics (e.g., "Operating System – Deadlock")
- System recommends top 3 videos + top 3 reading resources
- Students can bookmark topics and give feedback (Helpful / Not Helpful)
- ML engine ranks resources using: `score = rating × 0.4 + view_count_normalized × 0.3 + feedback_score × 0.3`

---

## Model 1 — `Semester`

Fields:
- `id` — AutoField (primary key)
- `name` — CharField (max 50), e.g., "1st Semester", "5th Semester"
- `order` — IntegerField (for sorting, e.g., 1, 2, 3...)
- `is_active` — BooleanField (default True)
- `created_at` — DateTimeField (auto_now_add)

Requirements:
- `Meta`: order by `order` field
- `__str__`: return `self.name`

---

## Model 2 — `Subject`

Fields:
- `id` — AutoField
- `semester` — ForeignKey to `Semester` (CASCADE, related_name='subjects')
- `name` — CharField (max 100), e.g., "Operating System"
- `code` — CharField (max 20, blank/null), e.g., "CS301"
- `description` — TextField (blank/null)
- `is_active` — BooleanField (default True)
- `created_at` — DateTimeField (auto_now_add)

Requirements:
- `Meta`: order by `semester`, then `name`
- `__str__`: return `f"{self.name} ({self.semester.name})"`

---

## Model 3 — `Topic`

Fields:
- `id` — AutoField
- `subject` — ForeignKey to `Subject` (CASCADE, related_name='topics')
- `name` — CharField (max 150), e.g., "Deadlock"
- `slug` — SlugField (unique, auto-generated from name)
- `description` — TextField (blank/null)
- `tags` — CharField (max 300, blank/null) — comma-separated keywords for ML matching, e.g., "deadlock,os,process,deadlock detection"
- `search_keywords` — TextField (blank/null) — extra keywords for TF-IDF search
- `is_active` — BooleanField (default True)
- `created_at` — DateTimeField (auto_now_add)
- `updated_at` — DateTimeField (auto_now)

Requirements:
- Override `save()` to auto-generate `slug` from `name` using `slugify`
- `Meta`: order by `name`
- `__str__`: return `f"{self.subject.name} – {self.name}"`
- Add a property `full_name` that returns `f"{self.subject.name} – {self.name}"`
- Add a property `tag_list` that returns `self.tags.split(',')` as a cleaned list

---

## Model 4 — `VideoResource`

Fields:
- `id` — AutoField
- `topic` — ForeignKey to `Topic` (CASCADE, related_name='videos')
- `title` — CharField (max 200)
- `description` — TextField
- `youtube_url` — URLField
- `youtube_video_id` — CharField (max 20, blank/null) — extracted from URL
- `thumbnail_url` — URLField (blank/null)
- `duration` — CharField (max 10), e.g., "18:42"
- `duration_seconds` — IntegerField (default 0) — for sorting
- `difficulty_level` — CharField with choices:
  ```python
  DIFFICULTY_CHOICES = [
      ('beginner', 'Beginner'),
      ('intermediate', 'Intermediate'),
      ('advanced', 'Advanced'),
  ]
  ```
  default = 'beginner'
- `view_count` — IntegerField (default 0)
- `rating` — FloatField (default 0.0) — 0 to 5
- `student_helpful_count` — IntegerField (default 0)
- `student_not_helpful_count` — IntegerField (default 0)
- `ml_score` — FloatField (default 0.0) — pre-calculated recommendation score
- `is_active` — BooleanField (default True)
- `created_at` — DateTimeField (auto_now_add)
- `updated_at` — DateTimeField (auto_now)

Requirements:
- Override `save()` to auto-extract `youtube_video_id` from `youtube_url` using regex or string parsing
- Override `save()` to auto-set `thumbnail_url` from video ID: `https://img.youtube.com/vi/{video_id}/hqdefault.jpg`
- Add property `feedback_score` that returns: `helpful / (helpful + not_helpful)` ratio, handling division by zero
- Add property `difficulty_color` returning css class string: `'beginner'→'green'`, `'intermediate'→'orange'`, `'advanced'→'red'`
- Add method `calculate_ml_score()` that computes: `rating * 0.4 + (view_count / 1_000_000) * 0.3 + feedback_score * 0.3` and saves it
- `Meta`: order by `-ml_score`
- `__str__`: return title

---

## Model 5 — `ReadingResource`

Fields:
- `id` — AutoField
- `topic` — ForeignKey to `Topic` (CASCADE, related_name='readings')
- `title` — CharField (max 200)
- `description` — TextField
- `url` — URLField
- `resource_type` — CharField with choices:
  ```python
  TYPE_CHOICES = [
      ('pdf', 'PDF Textbook'),
      ('blog', 'Blog Article'),
      ('notes', 'Study Notes'),
      ('article', 'Article'),
  ]
  ```
- `source_name` — CharField (max 100, blank/null), e.g., "GeeksForGeeks", "Silberschatz Textbook"
- `rating` — FloatField (default 0.0)
- `view_count` — IntegerField (default 0)
- `student_helpful_count` — IntegerField (default 0)
- `student_not_helpful_count` — IntegerField (default 0)
- `ml_score` — FloatField (default 0.0)
- `is_active` — BooleanField (default True)
- `created_at` — DateTimeField (auto_now_add)
- `updated_at` — DateTimeField (auto_now)

Requirements:
- Add property `feedback_score` same as VideoResource
- Add property `type_icon` returning icon identifier string per type
- Add property `type_color` returning color class per type
- Add method `calculate_ml_score()` same formula as VideoResource
- `Meta`: order by `-ml_score`
- `__str__`: return `f"{self.title} ({self.resource_type})"`

---

## Model 6 — `StudentInteraction`

Fields:
- `id` — AutoField
- `session_key` — CharField (max 40) — Django session key to identify user without login
- `topic` — ForeignKey to `Topic` (CASCADE, related_name='interactions')
- `resource_type` — CharField with choices: `('video', 'Video'), ('reading', 'Reading')`
- `resource_id` — IntegerField — ID of the video or reading resource
- `interaction_type` — CharField with choices:
  ```python
  INTERACTION_CHOICES = [
      ('bookmark', 'Bookmark'),
      ('helpful', 'Helpful'),
      ('not_helpful', 'Not Helpful'),
      ('view', 'Viewed'),
  ]
  ```
- `created_at` — DateTimeField (auto_now_add)

Requirements:
- `Meta`: `unique_together = [('session_key', 'topic', 'resource_type', 'resource_id', 'interaction_type')]`
- `Meta`: order by `-created_at`
- `__str__`: return `f"Session {self.session_key[:8]}... → {self.interaction_type} on {self.topic.name}"`

---

## After All Models

1. Write the complete `website/admin.py` that registers ALL models with these `ModelAdmin` classes:

   - `SemesterAdmin`: list_display = name, order, is_active
   - `SubjectAdmin`: list_display = name, semester, code, is_active; list_filter = semester; search_fields = name, code
   - `TopicAdmin`: list_display = name, subject, slug, is_active; list_filter = subject__semester, subject; search_fields = name, tags; prepopulated_fields = {'slug': ('name',)}
   - `VideoResourceAdmin`: list_display = title, topic, difficulty_level, rating, view_count, ml_score, is_active; list_filter = difficulty_level, topic__subject, is_active; search_fields = title
   - `ReadingResourceAdmin`: list_display = title, topic, resource_type, rating, ml_score, is_active; list_filter = resource_type, is_active; search_fields = title
   - `StudentInteractionAdmin`: list_display = session_key, topic, interaction_type, resource_type, created_at; list_filter = interaction_type, resource_type

2. Write the exact terminal commands to:
   ```bash
   python manage.py makemigrations website
   python manage.py migrate
   ```

3. Show the expected terminal output after successful migration.

4. List **5 common migration errors** and exact fixes.

---

## Output Requirements

- Complete `models.py` — every field, every method, every import
- Complete `admin.py` — every class registered
- All imports at top (django.db.models, slugify, re, etc.)
- Every method must have a docstring comment
- Production-ready code, no shortcuts
