# Prompt 05 — Views, URLs & Forms (`views.py`)

## Your Task

You are a senior Django developer. I am building **Topiq** — a Smart Learning Resource Recommendation System. My models and recommender engine are ready. Now write the **complete `website/views.py`**, **complete `website/urls.py`**, and **complete `website/forms.py`** with all views, logic, and URL patterns. Every line must be copy-paste ready.

---

## Project Context

**Already built:**
- `website/models.py` — Semester, Subject, Topic, VideoResource, ReadingResource, StudentInteraction
- `website/recommender.py` — `search_topics(query)` function that returns recommendation dict

**Import statement to use in views.py:**
```python
from website.recommender import search_topics, get_all_semesters
from website.models import Topic, VideoResource, ReadingResource, StudentInteraction, Semester
```

---

## View 1 — `index(request)` — Homepage

**URL:** `/`  
**Method:** GET  
**Template:** `website/index.html`

Logic:
1. Get all active `Semester` objects ordered by `order` field
2. Get any recent searches from session: `request.session.get('recent_searches', [])`
3. Get total resource count from DB: `VideoResource.objects.filter(is_active=True).count() + ReadingResource.objects.filter(is_active=True).count()`
4. Pass to template:
   ```python
   context = {
       'semesters': semesters,
       'recent_searches': recent_searches[-5:],  # last 5
       'total_resources': total_resources,
       'page_title': 'Topiq – Smart Study Resource Finder',
   }
   ```

---

## View 2 — `search_results(request)` — Main Search View

**URL:** `/search/`  
**Method:** GET  
**Template:** `website/results.html`

Logic (step by step):
1. Get `query = request.GET.get('q', '').strip()`
2. Get `semester_id = request.GET.get('semester', None)`
3. If `query` is empty → redirect to `index` with error message
4. If `len(query) < 2` → redirect with message "Please enter at least 2 characters"
5. Call `result = search_topics(query)`
6. Save query to session's recent searches list (max 10, no duplicates)
7. If `result['found']` is False → render `results.html` with `no_results=True`
8. Build `bookmarked_topics` list from session: `request.session.get('bookmarks', [])`
9. Pass full context to template:
   ```python
   context = {
       'query': query,
       'result': result,
       'videos': result.get('videos', []),
       'readings': result.get('readings', []),
       'matched_topic': result.get('matched_topic'),
       'similar_topics': result.get('similar_topics', []),
       'avg_study_time': result.get('avg_study_time', ''),
       'semester_name': result.get('semester_name', ''),
       'subject_name': result.get('subject_name', ''),
       'total_resources': result.get('total_resources', 0),
       'confidence_score': result.get('confidence_score', 0),
       'no_results': not result.get('found', False),
       'bookmarked_topics': bookmarked_topics,
       'semesters': get_all_semesters(),
       'page_title': f'{query} – Topiq Results',
   }
   ```

---

## View 3 — `api_search(request)` — AJAX JSON Search

**URL:** `/api/search/`  
**Method:** GET  
**Returns:** JSON

Logic:
1. Get `query = request.GET.get('q', '').strip()`
2. If empty → return `JsonResponse({'error': 'Empty query'}, status=400)`
3. Call `result = search_topics(query)`
4. Serialize result — extract only serializable fields (no Django model objects):
   ```python
   data = {
       'found': result['found'],
       'query': query,
       'matched_topic_name': result.get('matched_topic_name', ''),
       'subject_name': result.get('subject_name', ''),
       'semester_name': result.get('semester_name', ''),
       'videos': [
           {
               'id': v.id,
               'title': v.title,
               'description': v.description,
               'youtube_url': v.youtube_url,
               'thumbnail_url': v.thumbnail_url,
               'duration': v.duration,
               'difficulty_level': v.difficulty_level,
               'rating': v.rating,
           }
           for v in result.get('videos', [])
       ],
       'readings': [
           {
               'id': r.id,
               'title': r.title,
               'description': r.description,
               'url': r.url,
               'resource_type': r.resource_type,
               'source_name': r.source_name,
               'rating': r.rating,
           }
           for r in result.get('readings', [])
       ],
       'total_resources': result.get('total_resources', 0),
       'avg_study_time': result.get('avg_study_time', ''),
   }
   ```
5. Return `JsonResponse(data)`

---

## View 4 — `ai_chat(request)` — AI Assistant

**URL:** `/api/chat/`  
**Method:** POST  
**Returns:** JSON  
**CSRF:** Required (include `@csrf_exempt` NOT — use Django CSRF properly via JS header)

Logic:
1. Check `request.method == 'POST'` else return 405
2. Parse `import json; body = json.loads(request.body)`
3. Get `message = body.get('message', '').strip()`
4. Get `topic_context = body.get('topic_context', '')`
5. If empty message → return `JsonResponse({'error': 'Empty message'}, status=400)`
6. Build system prompt:
   ```
   You are an academic study assistant for university students using the Topiq platform.
   You ONLY answer university-level academic questions related to computer science, engineering, and related subjects.
   If asked about {topic_context}, give a clear, educational explanation.
   Do NOT answer questions about personal advice, politics, entertainment, or anything non-academic.
   If a non-academic question is asked, politely decline and ask for an academic question.
   Keep answers concise, clear, and student-friendly. Use bullet points and examples when helpful.
   ```
7. Call Anthropic API:
   ```python
   import os, requests
   
   api_key = os.environ.get('ANTHROPIC_API_KEY', '')
   headers = {
       'Content-Type': 'application/json',
       'x-api-key': api_key,
       'anthropic-version': '2023-06-01',
   }
   payload = {
       'model': 'claude-3-haiku-20240307',
       'max_tokens': 500,
       'system': system_prompt,
       'messages': [{'role': 'user', 'content': message}]
   }
   response = requests.post('https://api.anthropic.com/v1/messages', json=payload, headers=headers, timeout=30)
   ```
8. Parse response: `ai_reply = response.json()['content'][0]['text']`
9. Handle API errors — return fallback message if API fails
10. Return `JsonResponse({'reply': ai_reply, 'status': 'ok'})`

---

## View 5 — `bookmark_topic(request)` — Bookmark a Topic

**URL:** `/bookmark/`  
**Method:** POST  
**Returns:** JSON

Logic:
1. Parse POST body: `topic_id = body.get('topic_id')`
2. Get topic from DB or return 404
3. Check session bookmarks list: `bookmarks = request.session.get('bookmarks', [])`
4. If topic_id already in bookmarks → remove it (unbookmark), set `action = 'removed'`
5. Else → add to bookmarks list, set `action = 'added'`
6. Save back: `request.session['bookmarks'] = bookmarks`
7. Also save to `StudentInteraction` model
8. Return:
   ```python
   JsonResponse({
       'status': 'ok',
       'action': action,  # 'added' or 'removed'
       'topic_id': topic_id,
       'topic_name': topic.name,
       'bookmark_count': len(bookmarks)
   })
   ```

---

## View 6 — `submit_feedback(request)` — Helpful / Not Helpful

**URL:** `/feedback/`  
**Method:** POST  
**Returns:** JSON

Logic:
1. Parse POST body: `resource_type`, `resource_id`, `feedback_type` (helpful/not_helpful)
2. Get or ensure session key exists: `if not request.session.session_key: request.session.create()`
3. Create or update `StudentInteraction`:
   ```python
   interaction, created = StudentInteraction.objects.get_or_create(
       session_key=request.session.session_key,
       resource_type=resource_type,
       resource_id=resource_id,
       defaults={'interaction_type': feedback_type, 'topic_id': topic_id}
   )
   ```
4. If not created and different feedback → update `interaction_type`
5. Update the resource's `student_helpful_count` or `student_not_helpful_count`
6. Recalculate `ml_score` on that resource
7. Return:
   ```python
   JsonResponse({
       'status': 'ok',
       'feedback': feedback_type,
       'resource_id': resource_id,
       'helpful_count': resource.student_helpful_count,
   })
   ```

---

## `website/forms.py`

Create a simple `SearchForm`:
```python
class SearchForm(forms.Form):
    q = forms.CharField(
        min_length=2,
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search your study topic… e.g. Deadlock, Binary Tree',
            'class': 'search-input',
            'autocomplete': 'off',
        })
    )
    semester = forms.ModelChoiceField(
        queryset=None,  # set in __init__
        required=False,
        empty_label="All Semesters"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from website.models import Semester
        self.fields['semester'].queryset = Semester.objects.filter(is_active=True).order_by('order')
```

---

## `website/urls.py` — Complete

```python
from django.urls import path
from website import views

app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_results, name='search_results'),
    path('api/search/', views.api_search, name='api_search'),
    path('api/chat/', views.ai_chat, name='ai_chat'),
    path('bookmark/', views.bookmark_topic, name='bookmark_topic'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
]
```

---

## Error Handling in Every View

Every view must:
- Wrap logic in `try/except` 
- Log errors using Python logging
- Return appropriate HTTP status codes
- Never crash the server — always return a response

---

## Output Requirements

- Complete `views.py` — all 6 views, every import, no shortcuts
- Complete `forms.py`
- Complete `urls.py`
- All CSRF handling correct
- All JSON responses have consistent structure
- All error cases handled
- Add `# — VIEW: name —` comment before each view function
