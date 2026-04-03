# Prompt 04 — ML Recommendation Engine (`recommender.py`)

## Your Task

You are a senior Python developer and ML engineer. I am building a Django app called **Topiq**. Now I need you to create the complete **ML-powered recommendation engine** as `website/recommender.py`.

This is the brain of the project. Write it completely — no shortcuts, no partial code, every function fully implemented and commented.

---

## Project Context

- App: `website` (Django)
- Models available: `Topic`, `VideoResource`, `ReadingResource`, `StudentInteraction`
- Goal: Given a search query (e.g., "Binary Tree" or "tree data structure"), find the best matching topic and return top 3 videos and top 3 reading resources, ranked by ML score
- ML Tools: `scikit-learn` (TF-IDF + cosine similarity)

---

## What `recommender.py` Must Do

### Feature 1 — Topic Name Matching with TF-IDF

The system must handle these cases:
- Exact match: "Deadlock" → finds "Deadlock" topic
- Partial match: "dead lock" → finds "Deadlock"
- Synonym match: "Binary Tree" vs "Tree in DS" → both return same topic
- Case insensitive: "DEADLOCK" = "deadlock"
- Prefix match: "bank algo" → "Banker's Algorithm"

**How it works:**
1. Load all `Topic` names + their `tags` + `search_keywords` from DB
2. Build a TF-IDF matrix from all topic text
3. Vectorize the search query
4. Compute cosine similarity between query and all topics
5. Return top N matching topics above a similarity threshold

---

## Class: `ResourceRecommender`

Create a class with these methods:

### `__init__(self)`
- Initialize the TF-IDF vectorizer
- Set similarity threshold = 0.15
- Set top_n = 3

### `_build_topic_corpus(self)`
- Query all active topics from DB
- For each topic, create a document string: `f"{topic.name} {topic.subject.name} {topic.tags or ''} {topic.search_keywords or ''} {topic.description or ''}"`
- Return list of (topic_id, document_string)

### `find_matching_topics(self, query: str, top_n: int = 5) -> list`
- Take raw search query
- Call `_build_topic_corpus()`
- Fit TF-IDF on corpus
- Transform query
- Compute cosine similarity
- Return top_n topic IDs above threshold, sorted by similarity score
- Handle edge case: if no results above threshold, return partial matches

### `get_recommendations(self, query: str) -> dict`
This is the **main method** that returns the full recommendation result:

```python
def get_recommendations(self, query: str) -> dict:
    """
    Returns:
    {
        'query': 'Operating System – Deadlock',
        'matched_topic': <Topic object or None>,
        'matched_topic_name': 'Deadlock',
        'subject_name': 'Operating System',
        'semester_name': '5th Semester',
        'videos': [<VideoResource>, <VideoResource>, <VideoResource>],
        'readings': [<ReadingResource>, <ReadingResource>, <ReadingResource>],
        'similar_topics': [<Topic>, <Topic>],
        'total_resources': 6,
        'avg_study_time': '2.5 hrs',
        'confidence_score': 0.87,
        'found': True
    }
    """
```

Steps inside `get_recommendations()`:
1. Call `find_matching_topics(query)`
2. If no match found → return dict with `found: False`
3. Get best matched `Topic` from DB
4. Get `VideoResource.objects.filter(topic=topic, is_active=True).order_by('-ml_score')[:3]`
5. Get `ReadingResource.objects.filter(topic=topic, is_active=True).order_by('-ml_score')[:3]`
6. Calculate average study time from video durations
7. Get 2–3 similar topics from the same subject (exclude current topic)
8. Return full dict

### `calculate_avg_study_time(self, videos: list) -> str`
- Takes list of VideoResource objects
- Parses `duration` field (format "18:42") into seconds
- Sums all durations
- Converts to hours and minutes
- Returns formatted string: "1.5 hrs" or "45 min"

### `update_ml_scores(self)`
- Loop through all VideoResource and ReadingResource objects
- Call `resource.calculate_ml_score()` on each
- Save updated scores
- Return count of updated resources

### `get_feedback_score(self, resource_type: str, resource_id: int) -> float`
- Count `StudentInteraction` objects where resource_type=resource_type, resource_id=resource_id
- Count helpful vs not_helpful
- Return ratio: `helpful / (helpful + not_helpful + 1)` — add 1 to avoid division by zero

---

## Standalone Function: `search_topics(query)`

Outside the class, write a simple function that:
- Creates a `ResourceRecommender` instance
- Calls `get_recommendations(query)`
- Returns the result dict

This is the function `views.py` will import and use:

```python
from website.recommender import search_topics

result = search_topics("Operating System Deadlock")
```

---

## Standalone Function: `get_all_semesters()`

Returns all active `Semester` objects ordered by `order` field. Used in homepage view.

---

## Standalone Function: `get_subjects_by_semester(semester_id)`

Returns all active `Subject` objects for a given semester.

---

## Standalone Function: `get_topics_by_subject(subject_id)`

Returns all active `Topic` objects for a given subject.

---

## Error Handling Requirements

Every method must handle:
- Empty database (no topics) → return empty/safe result
- `scikit-learn` not installed → catch ImportError, fall back to simple string matching
- DB query errors → catch and log, return safe fallback
- Query too short (< 2 chars) → return `{'found': False, 'message': 'Query too short'}`

---

## Fallback: Simple String Matching

If scikit-learn is unavailable, implement a fallback `_simple_search(query)` method:
- Convert query to lowercase
- Filter topics where `name__icontains=query` OR `tags__icontains=query`
- Return first match

---

## Logging

Add Python `logging` throughout:
```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"Search query: {query}")
logger.info(f"Matched topic: {matched_topic}")
logger.warning("No topics found in database")
```

---

## Test the Recommender

After writing the class, add a `if __name__ == '__main__':` block at the bottom that:
- Sets up Django settings manually
- Runs 3 test searches:
  - `"deadlock"`
  - `"binary tree"`
  - `"sorting algorithm"`
- Prints results in readable format

---

## Required Imports

```python
import os
import re
import logging
import django
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
```

---

## Output Requirements

- Complete `recommender.py` — every class, every method, every function
- All edge cases handled
- All methods commented with docstrings
- Logging added throughout
- Fallback for missing sklearn
- Test block at bottom
