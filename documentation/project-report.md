# Topiq — Smart Learning Resource Recommendation System

## Cover Page

Project Title: Topiq — Smart Learning Resource Recommendation System  
Submitted by: [Your Name]  
Student ID: [Your ID]  
Department: Computer Science & Engineering  
University: [University Name]  
Supervisor: [Supervisor Name]  
Submission Date: [Date]  

---

## Abstract

Topiq is a topic-based smart learning resource recommendation system designed to reduce the time university students spend searching for quality study materials across multiple platforms. In a typical study workflow, students manually browse video platforms, blogs, notes repositories, and PDF resources to understand one academic concept. This fragmented approach leads to information overload, inconsistent quality, and inefficient study sessions. Topiq addresses this problem by providing a single Django-based web application where a student can search for a topic and instantly receive a ranked set of high-value learning resources.

The project combines traditional web engineering with lightweight machine learning. The backend is built with Django and SQLite, while the recommendation engine uses TF-IDF vectorization and cosine similarity to match user queries against topic names, tags, descriptions, and search keywords. After identifying the best-matching topic, the system ranks the associated resources using a weighted scoring formula that considers rating, normalized view count, and student feedback. The system also includes bookmark support, a session-based feedback loop, and an AI-powered study assistant integrated through the Anthropic Claude API for short academic explanations.

The implementation demonstrates that a focused, lightweight recommendation system can provide strong practical value without the infrastructure complexity of a full-scale LMS. The final system includes a responsive dark-themed frontend, seeded academic data, integration tests, caching, logging, and deployment-ready configuration. Results show that the platform successfully returns relevant resources for topic searches such as “Deadlock” and “Binary Tree,” while also supporting iterative ranking improvements through feedback. Topiq concludes that a compact, topic-centered educational recommendation system can significantly improve study efficiency for university learners.

---

## Chapter 1 — Introduction

### 1.1 Background

Students in university-level technical programs regularly depend on multiple digital sources to learn one topic effectively. A concept such as deadlock, dynamic programming, or normalization may require a quick video explanation, a detailed article, and short revision notes. Existing learning environments often organize content by course or instructor rather than by the exact concept a student wants to learn at a given moment.

### 1.2 Problem Statement

The main problem addressed in this project is the lack of a lightweight, topic-focused system that helps students find the best learning resources for a specific academic concept quickly. Students often search manually across YouTube, blogs, PDFs, and lecture notes, then compare multiple low-quality or duplicate resources before choosing one that appears useful. This wastes study time and increases cognitive load.

Another issue is that many existing educational platforms are not optimized for flexible query-based resource discovery. A student might type “dead lock,” “banker algo,” or “tree in DS,” but keyword-only systems often fail to connect these inputs to the intended topic. Without intelligent matching and ranking, search quality remains inconsistent, especially for short academic phrases and synonym-like variations.

### 1.3 Objectives

1. To build a centralized platform for topic-based academic resource discovery.
2. To recommend top-ranked videos and reading resources for each topic.
3. To use TF-IDF-based query matching for flexible academic search input.
4. To rank resources using ratings, popularity, and student feedback.
5. To provide an AI-based academic study assistant for short explanations.
6. To create a clean, responsive, and testable Django web application suitable for university submission.

### 1.4 Scope of the Project

The scope of Topiq includes topic search, resource recommendation, bookmark handling, anonymous feedback collection, seeded academic data, and a responsive web interface. The project is focused on university-level computer science and engineering topics and is not intended to replace a full learning management system. It is a concept-centric discovery platform rather than a content hosting platform.

### 1.5 Report Organization

This report is organized into six chapters. Chapter 1 introduces the project. Chapter 2 reviews related educational systems and recommendation approaches. Chapter 3 explains the system design and methodology. Chapter 4 presents implementation details. Chapter 5 discusses testing and results. Chapter 6 concludes the project and proposes future improvements.

---

## Chapter 2 — Literature Review

Learning management systems such as Moodle have long been used in universities to organize course materials, assignments, and communication. These platforms are powerful for classroom administration, but they are not primarily optimized for topic-first discovery. Students usually access resources through course hierarchies, week labels, or uploaded files rather than through intelligent search centered on a concept.

Massive open online course platforms such as Coursera and Khan Academy provide structured learning experiences with strong content quality and course sequencing. However, these platforms are often broad and platform-specific. They may not help a university student quickly compare a concept across a short explanatory video, a revision note, and a PDF chapter in one lightweight interface.

Educational recommendation systems have increasingly used machine learning methods to personalize learning support. Common approaches include collaborative filtering, content-based filtering, hybrid recommenders, and natural language matching. For small-to-medium academic projects, a content-based method is often more practical because it does not require large user-history datasets. TF-IDF remains a strong baseline for lightweight educational retrieval because it is simple, interpretable, and effective on structured topic metadata.

The gap addressed by Topiq is the need for a compact, searchable academic resource system that works at the topic level rather than the course level. Instead of attempting to replace existing LMS platforms, Topiq complements them by helping students discover study resources faster. This project fills that gap with a focused, explainable, and implementation-friendly solution based on Django, structured metadata, and ML-assisted ranking.

---

## Chapter 3 — System Design & Methodology

### 3.1 System Architecture

Topiq follows a request-response web architecture. A user submits a topic query through the browser. Django receives the request, routes it to a view, then calls the recommendation engine. The recommender retrieves topic metadata from the database, builds a TF-IDF search representation, selects the best matching topic, fetches associated ranked resources, and returns a result dictionary to the view. The view then renders the results page or returns JSON for AJAX endpoints.

System flow:

```text
User -> Browser -> Django View -> Recommender -> Database -> View Context -> HTML/JSON Response
```

### 3.2 Technology Stack

| Technology | Purpose | Version |
|---|---|---|
| Python | Core programming language | 3.11+ |
| Django | Backend framework | 4.2.16 |
| SQLite | Lightweight relational database | Built-in |
| scikit-learn | TF-IDF and cosine similarity | 1.4.2 |
| NumPy | Numerical utilities | 1.26.4 |
| Requests | Anthropic API communication | 2.31.0 |
| python-dotenv | Environment variable loading | 1.0.1 |
| Pillow | Image support dependency | 10.4.0 |
| HTML/CSS/JavaScript | Frontend implementation | Modern browser support |

### 3.3 Database Design

The database contains six core models. `Semester` stores academic semester labels and ordering. `Subject` groups topics under a semester. `Topic` represents the searchable academic concept and stores tags, descriptions, and keyword text for matching. `VideoResource` stores video content for a topic. `ReadingResource` stores PDFs, blogs, notes, and articles. `StudentInteraction` records bookmark and feedback actions using a session key instead of requiring login.

Relationship overview:

```text
Semester -> Subject -> Topic -> VideoResource
                          -> ReadingResource
                          -> StudentInteraction
```

### 3.4 ML Recommendation Engine

Topiq uses TF-IDF to represent topic text and cosine similarity to compare a user query against the topic corpus. Each topic document includes the topic name, subject name, tags, search keywords, and description. This improves flexibility for exact matches, partial matches, and related phrases.

The resource ranking formula is:

```text
score = rating × 0.4 + normalized_view_count × 0.3 + feedback_score × 0.3
```

These weights were chosen to balance three practical signals. Rating reflects perceived quality, view count reflects popularity and credibility, and feedback score reflects local usefulness inside the system. Rating receives the highest weight because resource quality matters more than raw popularity alone. Feedback is included to support a ranking loop that improves over time as students interact with the system.

The feedback loop works by collecting helpful and not-helpful interactions per resource. When a student submits feedback, the resource counts are updated and the ML score is recalculated. This means future searches can reflect actual student usefulness instead of relying only on static seed values.

### 3.5 System Flow Diagrams

Search flow:

```text
User enters query
    ->
search_results view
    ->
search_topics(query)
    ->
TF-IDF topic matching
    ->
best topic found
    ->
fetch top 3 videos + top 3 readings
    ->
render results page
```

Feedback loop:

```text
User clicks Helpful/Not Helpful
    ->
/feedback/ endpoint
    ->
StudentInteraction saved
    ->
resource counters updated
    ->
ml_score recalculated
    ->
future searches use updated ranking
```

---

## Chapter 4 — Implementation

### 4.1 Development Environment Setup

The project was developed in a Python virtual environment using Django 4.2. Environment variables are loaded from a `.env` file using `python-dotenv`. Dependencies are installed from `requirements.txt`.

```bash
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

### 4.2 Backend Implementation

The backend is organized around Django models, views, and a recommendation module. The models define the academic hierarchy and resources. Views handle HTML rendering and AJAX endpoints for search, AI chat, feedback, and bookmarks. The recommender is implemented as a service class that builds the topic corpus, computes similarity, and returns structured result data.

Key scoring logic:

```python
normalized_views = self.view_count / 1_000_000
self.ml_score = (self.rating * 0.4) + (normalized_views * 0.3) + (self.feedback_score * 0.3)
```

### 4.3 Frontend Implementation

The frontend uses Django templates for server-side rendering, a custom dark-themed CSS design, and vanilla JavaScript for interactive features. The base template contains the fixed header, global search, AI chat shell, and footer. The homepage introduces the system, while the results page shows videos, readings, feedback actions, bookmarks, and related topics.

### 4.4 AI Chat Integration

The AI assistant endpoint accepts a POST request, builds a constrained academic system prompt, and forwards the request to the Anthropic Messages API. If the API key is missing or the network request fails, the system returns a safe fallback reply instead of crashing.

```python
payload = {
    "model": "claude-3-haiku-20240307",
    "max_tokens": 500,
    "system": system_prompt,
    "messages": [{"role": "user", "content": message}],
}
```

### 4.5 Database Seeding

A custom Django management command seeds six semesters, eight subjects, twenty topics, and one hundred twenty resources. The command supports `--flush` and `--demo` modes, avoids duplicates, and recalculates ML scores after insertion.

AJAX feedback example:

```javascript
await fetch("/feedback/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": getCsrfToken(),
  },
  body: JSON.stringify({
    resource_type: "video",
    resource_id: 1,
    feedback_type: "helpful",
    topic_id: 1,
  }),
});
```

TF-IDF query example:

```python
topic_matrix = self.vectorizer.fit_transform(documents)
query_vector = self.vectorizer.transform([normalized_query])
similarities = cosine_similarity(query_vector, topic_matrix).flatten()
```

---

## Chapter 5 — Testing & Results

### 5.1 Testing Methodology

Testing combined unit-level checks, integration testing, and manual functional testing. Django `TestCase` classes were used to verify model behavior, recommender output, view responses, session persistence, and management command execution. Manual testing was used for frontend behavior such as chat interaction, toast messages, and visual layout.

### 5.2 Test Cases Table

| Test ID | Test Case | Expected Result | Actual Result | Status |
|---------|-----------|----------------|---------------|--------|
| TC01 | Search `deadlock` | 3 videos + 3 readings shown | 3 videos + 3 readings | ✅ Pass |
| TC02 | Search `binary tree` | Matching Binary Tree topic | Binary Tree returned | ✅ Pass |
| TC03 | Search empty string | Redirect with message | Redirected | ✅ Pass |
| TC04 | API search returns JSON | JSON with `videos` and `readings` | JSON returned correctly | ✅ Pass |
| TC05 | Topic slug generation | Slug auto-created | Slug created correctly | ✅ Pass |
| TC06 | Video thumbnail generation | Thumbnail URL built from video ID | Thumbnail generated | ✅ Pass |
| TC07 | Helpful feedback submission | Interaction saved and count updated | Count increased | ✅ Pass |
| TC08 | Bookmark submission | Topic saved in session | Session updated | ✅ Pass |
| TC09 | AI chat without API key | Safe fallback response | Fallback returned | ✅ Pass |
| TC10 | Seed command demo mode | Demo data inserted | 36 resources created | ✅ Pass |

### 5.3 Performance Observations

The project performs well for a lightweight university dataset. Query matching is fast because the topic corpus is relatively small. Search performance improved further through `select_related()` optimization and local-memory caching of search results for repeated queries. Static assets are small and page rendering remains responsive on desktop and mobile.

### 5.4 Known Limitations

The current implementation uses content-based matching rather than personalized recommendations. The AI assistant depends on an external API and can fall back when unavailable. SQLite is sufficient for demonstration but is not ideal for high-concurrency production deployment. Search results are only as strong as the metadata quality assigned to each topic and resource.

---

## Chapter 6 — Conclusion & Future Work

### 6.1 Conclusion

Topiq successfully demonstrates how a focused academic recommendation system can improve study efficiency for university students. The project delivers a complete Django application with topic-based search, ranked video and reading recommendations, session-based feedback, bookmarking, seeded academic content, and an AI academic support feature.

From a software engineering perspective, the project integrates backend logic, machine learning, frontend interaction, testing, and deployment preparation into one coherent academic product. The architecture remains understandable and lightweight, which makes it suitable both for demonstration and for future extension.

The implemented TF-IDF recommender provides practical value by improving topic discovery beyond simple exact keyword matching. Resource ranking also becomes more meaningful by combining quality, popularity, and user feedback signals in a transparent formula. This makes the system not only functional, but also explainable.

Overall, the project meets its main academic and engineering goals. It shows that a concept-focused search and recommendation tool can serve as a useful study companion for technical education and can be extended further into a richer learning platform.

### 6.2 Future Work

- Collaborative filtering for personalized recommendations
- User accounts with CGPA-based content personalization
- Mobile app version
- Admin dashboard with analytics
- Integration with university LMS
- Multilingual support (Bengali + English)

---

## References

1. Django Software Foundation. Django Documentation. https://docs.djangoproject.com/
2. Scikit-learn Developers. Scikit-learn Documentation. https://scikit-learn.org/
3. Anthropic. Claude API Documentation. https://docs.anthropic.com/
4. Silberschatz, A., Galvin, P. B., and Gagne, G. Operating System Concepts.
5. Elmasri, R. and Navathe, S. Fundamentals of Database Systems.
6. Cormen, T. H., Leiserson, C. E., Rivest, R. L., and Stein, C. Introduction to Algorithms.
7. Manning, C. D., Raghavan, P., and Schütze, H. Introduction to Information Retrieval.
8. Russell, S. and Norvig, P. Artificial Intelligence: A Modern Approach.
9. Sommerville, I. Software Engineering.
10. General literature on educational recommendation systems and content-based filtering methods.

