# Prompt 08 — Seed Data & Management Command (`seed_data.py`)

## Your Task

You are a senior Django developer. I am building **Topiq** — a Smart Learning Resource Recommendation System. Write the **complete Django management command** `website/management/commands/seed_data.py` that populates the database with realistic sample data.

After running `python manage.py seed_data`, the app should have enough real data to fully demonstrate all features.

---

## File Location

```
website/
└── management/
    ├── __init__.py
    └── commands/
        ├── __init__.py
        └── seed_data.py    ← write this complete file
```

Also write the content of both `__init__.py` files (they are empty but must exist).

---

## Command Requirements

```bash
python manage.py seed_data          # seed all data (skip if already exists)
python manage.py seed_data --flush  # delete all existing data then re-seed
python manage.py seed_data --demo   # seed only demo data (faster, for testing)
```

The command must:
1. Print progress messages as it runs (colored terminal output using `self.style.SUCCESS`, `self.style.WARNING`)
2. Check if data already exists before inserting (avoid duplicates)
3. Use `bulk_create()` for efficiency
4. After seeding, print a summary of what was created

---

## Data to Seed

### Semesters (6 semesters)

```python
semesters = [
    {'name': '1st Semester', 'order': 1},
    {'name': '2nd Semester', 'order': 2},
    {'name': '3rd Semester', 'order': 3},
    {'name': '4th Semester', 'order': 4},
    {'name': '5th Semester', 'order': 5},
    {'name': '6th Semester', 'order': 6},
]
```

---

### Subjects (8 subjects spread across semesters)

```python
subjects = [
    {'name': 'Data Structures', 'code': 'CS201', 'semester': '3rd Semester'},
    {'name': 'Algorithms', 'code': 'CS202', 'semester': '3rd Semester'},
    {'name': 'Operating System', 'code': 'CS301', 'semester': '5th Semester'},
    {'name': 'Database Management System', 'code': 'CS302', 'semester': '5th Semester'},
    {'name': 'Computer Networks', 'code': 'CS303', 'semester': '5th Semester'},
    {'name': 'Object Oriented Programming', 'code': 'CS204', 'semester': '4th Semester'},
    {'name': 'Software Engineering', 'code': 'CS401', 'semester': '6th Semester'},
    {'name': 'Artificial Intelligence', 'code': 'CS402', 'semester': '6th Semester'},
]
```

---

### Topics (at least 20 topics total, 2–3 per subject)

For each subject, create 2–3 topics with realistic names, descriptions, and comma-separated tags:

**Data Structures:**
- Linked List — tags: "linked list, singly linked, doubly linked, circular"
- Binary Tree — tags: "binary tree, tree, BST, binary search tree, tree traversal"
- Sorting Algorithms — tags: "sorting, bubble sort, merge sort, quick sort, insertion sort, selection sort"

**Algorithms:**
- Dynamic Programming — tags: "dp, dynamic programming, memoization, tabulation, knapsack"
- Graph Algorithms — tags: "graph, BFS, DFS, shortest path, Dijkstra, Bellman-Ford"

**Operating System:**
- Deadlock — tags: "deadlock, coffman conditions, banker algorithm, deadlock detection, resource allocation, mutual exclusion"
- Process Scheduling — tags: "scheduling, FCFS, round robin, priority scheduling, SJF, CPU scheduling"
- Memory Management — tags: "memory, paging, segmentation, virtual memory, page replacement"

**Database Management System:**
- SQL Queries — tags: "SQL, select, join, group by, having, subquery, aggregate"
- Normalization — tags: "normalization, 1NF, 2NF, 3NF, BCNF, functional dependency"
- Transactions — tags: "transaction, ACID, concurrency control, deadlock in DBMS, isolation"

**Computer Networks:**
- OSI Model — tags: "OSI, seven layers, network model, TCP/IP, protocols"
- TCP vs UDP — tags: "TCP, UDP, transport layer, connection oriented, datagram"

**OOP:**
- Inheritance — tags: "inheritance, polymorphism, OOP, class, object, base class, derived class"
- Design Patterns — tags: "design patterns, singleton, factory, observer, SOLID"

**Software Engineering:**
- SDLC Models — tags: "SDLC, waterfall, agile, scrum, spiral model, software lifecycle"

**Artificial Intelligence:**
- Search Algorithms — tags: "AI search, BFS, DFS, A star, heuristic, uninformed search"
- Machine Learning Basics — tags: "machine learning, supervised, unsupervised, regression, classification, neural network"

---

### Video Resources (3 per topic = ~60 videos total)

For each topic, create 3 `VideoResource` objects with these details:

**Format for Deadlock topic (use similar pattern for all):**

```python
deadlock_videos = [
    {
        'title': 'Deadlock in Operating System – Full Explanation',
        'description': 'Covers all four necessary conditions of deadlock, with easy visual diagrams and real-world examples to help you understand from scratch.',
        'youtube_url': 'https://www.youtube.com/watch?v=onkWXaXAgbY',
        'duration': '18:42',
        'duration_seconds': 1122,
        'difficulty_level': 'beginner',
        'view_count': 245000,
        'rating': 4.7,
        'student_helpful_count': 89,
        'student_not_helpful_count': 4,
    },
    {
        'title': "Banker's Algorithm for Deadlock Avoidance – Step by Step",
        'description': "Detailed walkthrough of Banker's Algorithm with numerical examples. Perfect for exam-oriented practice and understanding resource allocation.",
        'youtube_url': 'https://www.youtube.com/watch?v=2V2FfP_olaA',
        'duration': '24:10',
        'duration_seconds': 1450,
        'difficulty_level': 'intermediate',
        'view_count': 198000,
        'rating': 4.5,
        'student_helpful_count': 73,
        'student_not_helpful_count': 8,
    },
    {
        'title': 'Deadlock Detection & Recovery – OS Concepts (Gate Exam Level)',
        'description': 'Advanced lecture covering detection algorithms, recovery strategies, and common university exam questions on deadlock scenarios.',
        'youtube_url': 'https://www.youtube.com/watch?v=UVo9MSGd9kE',
        'duration': '31:55',
        'duration_seconds': 1915,
        'difficulty_level': 'advanced',
        'view_count': 134000,
        'rating': 4.3,
        'student_helpful_count': 51,
        'student_not_helpful_count': 12,
    },
]
```

Write similar 3-video sets for ALL other topics (Binary Tree, Linked List, SQL, etc.) with realistic titles, descriptions, YouTube URLs (can use placeholder/realistic fake URLs), durations, and ratings.

---

### Reading Resources (3 per topic = ~60 readings total)

For each topic, create 3 `ReadingResource` objects — one PDF, one Blog, one Notes:

**Format for Deadlock topic:**

```python
deadlock_readings = [
    {
        'title': 'Operating System Concepts – Deadlock Chapter (Silberschatz)',
        'description': 'The classic OS textbook chapter covering deadlock characterization, prevention, avoidance and detection with detailed examples and exercises.',
        'url': 'https://os.ecci.ucr.ac.cr/slides/Abraham-Silberschatz-Operating-System-Concepts-10th-2018.pdf',
        'resource_type': 'pdf',
        'source_name': 'Silberschatz Textbook',
        'rating': 4.9,
        'view_count': 89000,
        'student_helpful_count': 120,
        'student_not_helpful_count': 5,
    },
    {
        'title': 'Understanding Deadlock: Conditions, Prevention & Avoidance Explained',
        'description': 'A well-illustrated blog post breaking down all deadlock conditions with diagrams, code snippets and practical interview questions for CS students.',
        'url': 'https://www.geeksforgeeks.org/introduction-of-deadlock-in-operating-system/',
        'resource_type': 'blog',
        'source_name': 'GeeksForGeeks',
        'rating': 4.6,
        'view_count': 340000,
        'student_helpful_count': 95,
        'student_not_helpful_count': 11,
    },
    {
        'title': "Deadlock – Short Notes & Formula Sheet for Exam Prep",
        'description': "Concise, exam-ready notes covering all key concepts, Banker's algorithm steps, and important definitions. Ideal for last-minute revision before exams.",
        'url': 'https://www.studocu.com/in/document/university-of-delhi/operating-system/deadlock-notes/12345',
        'resource_type': 'notes',
        'source_name': 'StudyNotes',
        'rating': 4.4,
        'view_count': 67000,
        'student_helpful_count': 78,
        'student_not_helpful_count': 9,
    },
]
```

Write similar reading sets for all other topics.

---

## After Seeding — Recalculate ML Scores

After all data is inserted, loop through all resources and call `calculate_ml_score()`:

```python
self.stdout.write('Recalculating ML scores...')
for video in VideoResource.objects.all():
    video.calculate_ml_score()
    video.save()

for reading in ReadingResource.objects.all():
    reading.calculate_ml_score()
    reading.save()
```

---

## Final Output Message

After seeding completes:
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
🚀 Run the server: python manage.py runserver
🔍 Try searching: "Deadlock" or "Binary Tree"
```

---

## Output Requirements

- Complete `seed_data.py` — the full management command class
- All data entries written out (no "add more here" placeholders)
- Uses `get_or_create()` to avoid duplicate entries on re-run
- `--flush` option deletes all records first
- Progress messages printed to terminal throughout
- ML scores recalculated after seeding
- Final summary printed with exact counts
