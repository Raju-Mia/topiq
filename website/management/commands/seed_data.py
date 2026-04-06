"""Seed realistic demo data for the Topiq project."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote_plus

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from website.models import ReadingResource, Semester, Subject, Topic, VideoResource


SEMESTER_DATA = [
    {"name": "1st Semester", "order": 1},
    {"name": "2nd Semester", "order": 2},
    {"name": "3rd Semester", "order": 3},
    {"name": "4th Semester", "order": 4},
    {"name": "5th Semester", "order": 5},
    {"name": "6th Semester", "order": 6},
]

SUBJECT_DATA = [
    {
        "name": "Data Structures",
        "code": "CS201",
        "semester": "3rd Semester",
        "description": "Core data organization techniques used across programming and systems.",
    },
    {
        "name": "Algorithms",
        "code": "CS202",
        "semester": "3rd Semester",
        "description": "Design and analysis of efficient computational problem-solving methods.",
    },
    {
        "name": "Operating System",
        "code": "CS301",
        "semester": "5th Semester",
        "description": "Concepts of process control, memory, resource allocation, and system design.",
    },
    {
        "name": "Database Management System",
        "code": "CS302",
        "semester": "5th Semester",
        "description": "Relational databases, SQL, transaction management, and schema design.",
    },
    {
        "name": "Computer Networks",
        "code": "CS303",
        "semester": "5th Semester",
        "description": "Network models, transport protocols, routing, and communication fundamentals.",
    },
    {
        "name": "Object Oriented Programming",
        "code": "CS204",
        "semester": "4th Semester",
        "description": "Object-oriented design, abstraction, and reusable software development practices.",
    },
    {
        "name": "Software Engineering",
        "code": "CS401",
        "semester": "6th Semester",
        "description": "Software process models, requirements, collaboration, and quality assurance.",
    },
    {
        "name": "Artificial Intelligence",
        "code": "CS402",
        "semester": "6th Semester",
        "description": "Search, reasoning, machine learning, and intelligent decision-making methods.",
    },
]

TOPIC_DATA = [
    {
        "subject": "Data Structures",
        "name": "Linked List",
        "description": "Understand singly, doubly, and circular linked lists along with insertion and deletion operations.",
        "tags": "linked list, singly linked, doubly linked, circular, node, pointer",
        "search_keywords": "linked list insertion deletion traversal pointers implementation",
    },
    {
        "subject": "Data Structures",
        "name": "Binary Tree",
        "description": "Study binary trees, BST properties, recursive traversal, and common interview-style problems.",
        "tags": "binary tree, tree, BST, binary search tree, tree traversal, preorder, inorder, postorder",
        "search_keywords": "binary tree recursion BST level order traversal balanced tree",
    },
    {
        "subject": "Data Structures",
        "name": "Sorting Algorithms",
        "description": "Compare classical sorting methods by time complexity, stability, and real-world use cases.",
        "tags": "sorting, bubble sort, merge sort, quick sort, insertion sort, selection sort",
        "search_keywords": "sorting algorithms complexity stable in-place divide and conquer",
    },
    {
        "subject": "Algorithms",
        "name": "Dynamic Programming",
        "description": "Learn to solve optimization problems using overlapping subproblems and state transitions.",
        "tags": "dp, dynamic programming, memoization, tabulation, knapsack, optimal substructure",
        "search_keywords": "dynamic programming recurrence relation top down bottom up",
    },
    {
        "subject": "Algorithms",
        "name": "Graph Algorithms",
        "description": "Explore traversal, shortest path, spanning trees, and graph representation techniques.",
        "tags": "graph, BFS, DFS, shortest path, Dijkstra, Bellman-Ford, MST",
        "search_keywords": "graph algorithms traversal shortest path weighted graph adjacency list",
    },
    {
        "subject": "Operating System",
        "name": "Deadlock",
        "description": "Covers deadlock conditions, avoidance, detection, and recovery strategies in operating systems.",
        "tags": "deadlock, coffman conditions, banker algorithm, deadlock detection, resource allocation, mutual exclusion",
        "search_keywords": "deadlock prevention avoidance banker algorithm circular wait operating system",
    },
    {
        "subject": "Operating System",
        "name": "Process Scheduling",
        "description": "Study CPU scheduling policies, waiting time, turnaround time, and performance trade-offs.",
        "tags": "scheduling, FCFS, round robin, priority scheduling, SJF, CPU scheduling",
        "search_keywords": "process scheduling gantt chart waiting time turnaround time preemptive",
    },
    {
        "subject": "Operating System",
        "name": "Memory Management",
        "description": "Learn paging, segmentation, virtual memory, and page replacement techniques.",
        "tags": "memory, paging, segmentation, virtual memory, page replacement, TLB",
        "search_keywords": "memory management address translation virtual memory demand paging",
    },
    {
        "subject": "Database Management System",
        "name": "SQL Queries",
        "description": "Practice retrieving, filtering, joining, and aggregating relational data with SQL.",
        "tags": "SQL, select, join, group by, having, subquery, aggregate",
        "search_keywords": "sql queries joins nested query group by aggregate functions",
    },
    {
        "subject": "Database Management System",
        "name": "Normalization",
        "description": "Understand normal forms, dependency analysis, and redundancy reduction in schemas.",
        "tags": "normalization, 1NF, 2NF, 3NF, BCNF, functional dependency",
        "search_keywords": "database normalization schema design normal forms functional dependency",
    },
    {
        "subject": "Database Management System",
        "name": "Transactions",
        "description": "Learn ACID properties, schedules, concurrency control, and isolation levels in DBMS.",
        "tags": "transaction, ACID, concurrency control, deadlock in DBMS, isolation, serializability",
        "search_keywords": "transactions ACID serial schedule concurrency control recovery",
    },
    {
        "subject": "Computer Networks",
        "name": "OSI Model",
        "description": "Break down the seven OSI layers and map common protocols to each communication stage.",
        "tags": "OSI, seven layers, network model, TCP/IP, protocols, layering",
        "search_keywords": "osi model layers network stack protocol suite encapsulation",
    },
    {
        "subject": "Computer Networks",
        "name": "TCP vs UDP",
        "description": "Compare reliable and unreliable transport communication with practical networking examples.",
        "tags": "TCP, UDP, transport layer, connection oriented, datagram, packet delivery",
        "search_keywords": "tcp vs udp socket transport layer reliability flow control",
    },
    {
        "subject": "Object Oriented Programming",
        "name": "Inheritance",
        "description": "Learn reuse and extensibility through inheritance, overriding, and polymorphism.",
        "tags": "inheritance, polymorphism, OOP, class, object, base class, derived class",
        "search_keywords": "inheritance polymorphism method overriding object oriented programming",
    },
    {
        "subject": "Object Oriented Programming",
        "name": "Design Patterns",
        "description": "Study common reusable OOP design solutions and where each pattern fits best.",
        "tags": "design patterns, singleton, factory, observer, SOLID, strategy pattern",
        "search_keywords": "design patterns oop factory observer singleton strategy principles",
    },
    {
        "subject": "Software Engineering",
        "name": "SDLC Models",
        "description": "Compare waterfall, agile, spiral, and iterative software development approaches.",
        "tags": "SDLC, waterfall, agile, scrum, spiral model, software lifecycle",
        "search_keywords": "sdlc models software process waterfall agile spiral incremental",
    },
    {
        "subject": "Software Engineering",
        "name": "Requirements Engineering",
        "description": "Understand elicitation, specification, validation, and stakeholder alignment in projects.",
        "tags": "requirements engineering, elicitation, specification, validation, stakeholder, use case",
        "search_keywords": "requirements gathering specification validation non functional requirements",
    },
    {
        "subject": "Artificial Intelligence",
        "name": "Search Algorithms",
        "description": "Study uninformed and heuristic search for problem solving in AI systems.",
        "tags": "AI search, BFS, DFS, A star, heuristic, uninformed search",
        "search_keywords": "ai search algorithms best first search heuristic path finding",
    },
    {
        "subject": "Artificial Intelligence",
        "name": "Machine Learning Basics",
        "description": "Get a foundational overview of supervised and unsupervised machine learning concepts.",
        "tags": "machine learning, supervised, unsupervised, regression, classification, neural network",
        "search_keywords": "machine learning basics dataset features labels model evaluation",
    },
    {
        "subject": "Artificial Intelligence",
        "name": "Knowledge Representation",
        "description": "Explore semantic networks, logic, rules, and representation of intelligent knowledge.",
        "tags": "knowledge representation, propositional logic, semantic network, inference, expert systems",
        "search_keywords": "knowledge representation first order logic semantic nets expert systems",
    },
]


@dataclass(frozen=True)
class ResourcePreset:
    """Template values used to generate topic resources consistently."""

    suffix: str
    description: str
    duration: str
    duration_seconds: int
    difficulty_level: str
    view_count: int
    rating: float
    helpful: int
    not_helpful: int


VIDEO_PRESETS = [
    ResourcePreset(
        suffix="Full Explanation",
        description="Beginner-friendly walkthrough covering the core ideas, key terminology, and simple examples for strong conceptual understanding.",
        duration="18:42",
        duration_seconds=1122,
        difficulty_level="beginner",
        view_count=245000,
        rating=4.7,
        helpful=89,
        not_helpful=4,
    ),
    ResourcePreset(
        suffix="Step by Step Problem Solving",
        description="Intermediate lesson focused on worked examples, exam patterns, and practical reasoning strategies students can apply quickly.",
        duration="24:10",
        duration_seconds=1450,
        difficulty_level="intermediate",
        view_count=198000,
        rating=4.5,
        helpful=73,
        not_helpful=8,
    ),
    ResourcePreset(
        suffix="Advanced Concepts and Exam Practice",
        description="Advanced treatment of the topic with deeper explanations, tricky cases, and university exam-style problem analysis.",
        duration="31:55",
        duration_seconds=1915,
        difficulty_level="advanced",
        view_count=134000,
        rating=4.3,
        helpful=51,
        not_helpful=12,
    ),
]

READING_PRESETS = [
    {
        "resource_type": "pdf",
        "title_suffix": "Comprehensive PDF Guide",
        "description": "Detailed textbook-style reading material that explains definitions, diagrams, theory, and worked examples in one place.",
        "source_name": "Topiq Reference PDF",
        "url": "https://example.com/resources/{slug}-guide.pdf",
        "rating": 4.9,
        "view_count": 89000,
        "helpful": 120,
        "not_helpful": 5,
    },
    {
        "resource_type": "blog",
        "title_suffix": "Concept Breakdown and Examples",
        "description": "Blog-style explanation with approachable language, visuals, and practical examples ideal for revision before class or exams.",
        "source_name": "GeeksForGeeks",
        "url": "https://www.geeksforgeeks.org/{slug}/",
        "rating": 4.6,
        "view_count": 340000,
        "helpful": 95,
        "not_helpful": 11,
    },
    {
        "resource_type": "notes",
        "title_suffix": "Short Notes and Exam Revision Sheet",
        "description": "Compact revision notes highlighting the most important formulas, steps, and definitions for quick exam preparation.",
        "source_name": "StudyNotes",
        "url": "https://www.studocu.com/in/document/topiq/{slug}/revision-notes/12345",
        "rating": 4.4,
        "view_count": 67000,
        "helpful": 78,
        "not_helpful": 9,
    },
]


def build_youtube_search_url(query: str) -> str:
    """Return a stable YouTube search URL for demo resource links."""
    return f"https://www.youtube.com/results?search_query={quote_plus(query)}"


class Command(BaseCommand):
    """Seed Topiq with realistic university learning data."""

    help = "Seed the database with semesters, subjects, topics, and sample resources."

    def add_arguments(self, parser):
        """Register command-line flags for seed behavior."""
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing seeded content before inserting fresh data.",
        )
        parser.add_argument(
            "--demo",
            action="store_true",
            help="Insert a smaller demo dataset for quicker local testing.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        """Run the full seeding workflow with duplicate-safe behavior."""
        flush = options["flush"]
        demo = options["demo"]

        if flush:
            self.stdout.write(self.style.WARNING("Flushing existing Topiq data..."))
            self._flush_existing_data()

        self.stdout.write(self.style.SUCCESS("Starting Topiq seed process..."))

        topic_data = TOPIC_DATA[:6] if demo else TOPIC_DATA

        semester_counts = self._seed_semesters()
        subject_counts = self._seed_subjects()
        topic_counts = self._seed_topics(topic_data)
        video_counts = self._seed_video_resources(topic_data)
        reading_counts = self._seed_reading_resources(topic_data)

        self.stdout.write("Recalculating ML scores...")
        self._recalculate_scores()

        self._print_summary(
            semester_counts["created"],
            subject_counts["created"],
            topic_counts["created"],
            video_counts["created"],
            reading_counts["created"],
        )

    def _flush_existing_data(self):
        """Delete seeded objects in dependency order."""
        ReadingResource.objects.all().delete()
        VideoResource.objects.all().delete()
        Topic.objects.all().delete()
        Subject.objects.all().delete()
        Semester.objects.all().delete()

    def _seed_semesters(self) -> dict[str, int]:
        """Insert semester records while skipping duplicates."""
        existing_names = set(Semester.objects.values_list("name", flat=True))
        to_create = [
            Semester(name=item["name"], order=item["order"], is_active=True)
            for item in SEMESTER_DATA
            if item["name"] not in existing_names
        ]
        if to_create:
            Semester.objects.bulk_create(to_create)
        self.stdout.write(self.style.SUCCESS(f"Semesters processed: {len(SEMESTER_DATA)}"))
        return {"created": len(to_create)}

    def _seed_subjects(self) -> dict[str, int]:
        """Insert subjects using semester names as the foreign-key lookup source."""
        semester_map = {semester.name: semester for semester in Semester.objects.all()}
        existing_names = set(Subject.objects.values_list("name", flat=True))

        to_create = []
        for item in SUBJECT_DATA:
            if item["name"] in existing_names:
                continue
            to_create.append(
                Subject(
                    semester=semester_map[item["semester"]],
                    name=item["name"],
                    code=item["code"],
                    description=item["description"],
                    is_active=True,
                )
            )

        if to_create:
            Subject.objects.bulk_create(to_create)
        self.stdout.write(self.style.SUCCESS(f"Subjects processed: {len(SUBJECT_DATA)}"))
        return {"created": len(to_create)}

    def _seed_topics(self, topic_data: list[dict]) -> dict[str, int]:
        """Insert topic records and let model save logic build unique slugs."""
        subject_map = {subject.name: subject for subject in Subject.objects.all()}
        existing_pairs = set(Topic.objects.values_list("subject__name", "name"))
        created = 0

        for item in topic_data:
            pair = (item["subject"], item["name"])
            if pair in existing_pairs:
                continue
            Topic.objects.create(
                subject=subject_map[item["subject"]],
                name=item["name"],
                description=item["description"],
                tags=item["tags"],
                search_keywords=item["search_keywords"],
                is_active=True,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Topics processed: {len(topic_data)}"))
        return {"created": created}

    def _seed_video_resources(self, topic_data: list[dict]) -> dict[str, int]:
        """Insert or refresh three video resources per topic using working YouTube search links."""
        topic_map = {topic.name: topic for topic in Topic.objects.select_related("subject")}
        created = 0

        for index, topic_item in enumerate(topic_data, start=1):
            topic = topic_map[topic_item["name"]]
            subject_label = topic.subject.name

            for preset in VIDEO_PRESETS:
                title = f"{topic.name} in {subject_label} – {preset.suffix}"
                if topic.name == "Deadlock":
                    deadlock_titles = {
                        "beginner": "Deadlock in Operating System – Full Explanation",
                        "intermediate": "Banker's Algorithm for Deadlock Avoidance – Step by Step",
                        "advanced": "Deadlock Detection & Recovery – OS Concepts (Gate Exam Level)",
                    }
                    title = deadlock_titles[preset.difficulty_level]

                search_query = " ".join(
                    [
                        topic.name,
                        subject_label,
                        preset.difficulty_level,
                        "tutorial",
                        "for students",
                    ]
                )
                _, was_created = VideoResource.objects.update_or_create(
                    topic=topic,
                    title=title,
                    defaults={
                        "description": f"{topic_item['description']} {preset.description}",
                        "youtube_url": build_youtube_search_url(search_query),
                        "duration": preset.duration,
                        "duration_seconds": preset.duration_seconds + (index * 7),
                        "difficulty_level": preset.difficulty_level,
                        "view_count": preset.view_count + (index * 1300),
                        "rating": max(4.0, round(preset.rating - (index % 3) * 0.05, 1)),
                        "student_helpful_count": preset.helpful + index,
                        "student_not_helpful_count": preset.not_helpful + (index % 4),
                        "is_active": True,
                    },
                )
                if was_created:
                    created += 1

        self.stdout.write(self.style.SUCCESS(f"Video resources processed: {len(topic_data) * 3}"))
        return {"created": created}

    def _seed_reading_resources(self, topic_data: list[dict]) -> dict[str, int]:
        """Insert or refresh PDF, blog, and notes reading resources for each topic."""
        topic_map = {topic.name: topic for topic in Topic.objects.select_related("subject")}
        created = 0

        for index, topic_item in enumerate(topic_data, start=1):
            topic = topic_map[topic_item["name"]]
            slug = slugify(topic.name)

            for preset in READING_PRESETS:
                title = f"{topic.name} – {preset['title_suffix']}"
                if topic.name == "Deadlock":
                    deadlock_titles = {
                        "pdf": "Operating System Concepts – Deadlock Chapter (Silberschatz)",
                        "blog": "Understanding Deadlock: Conditions, Prevention & Avoidance Explained",
                        "notes": "Deadlock – Short Notes & Formula Sheet for Exam Prep",
                    }
                    title = deadlock_titles[preset["resource_type"]]

                _, was_created = ReadingResource.objects.update_or_create(
                    topic=topic,
                    title=title,
                    defaults={
                        "description": f"{topic_item['description']} {preset['description']}",
                        "url": preset["url"].format(slug=slug),
                        "resource_type": preset["resource_type"],
                        "source_name": preset["source_name"],
                        "rating": max(4.0, round(preset["rating"] - (index % 3) * 0.05, 1)),
                        "view_count": preset["view_count"] + (index * 900),
                        "student_helpful_count": preset["helpful"] + index,
                        "student_not_helpful_count": preset["not_helpful"] + (index % 5),
                        "is_active": True,
                    },
                )
                if was_created:
                    created += 1

        self.stdout.write(self.style.SUCCESS(f"Reading resources processed: {len(topic_data) * 3}"))
        return {"created": created}

    def _recalculate_scores(self):
        """Refresh machine-learning scores after all records are present."""
        for video in VideoResource.objects.all():
            video.calculate_ml_score()
            video.save()

        for reading in ReadingResource.objects.all():
            reading.calculate_ml_score()
            reading.save()

    def _print_summary(
        self,
        semesters_created: int,
        subjects_created: int,
        topics_created: int,
        videos_created: int,
        readings_created: int,
    ):
        """Print the final seed summary using current database counts."""
        total_videos = VideoResource.objects.count()
        total_readings = ReadingResource.objects.count()

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("✅ Seed data complete!"))
        self.stdout.write("──────────────────────────────")
        self.stdout.write(f"Semesters created:    {Semester.objects.count()} ({semesters_created} new)")
        self.stdout.write(f"Subjects created:     {Subject.objects.count()} ({subjects_created} new)")
        self.stdout.write(f"Topics created:       {Topic.objects.count()} ({topics_created} new)")
        self.stdout.write(f"Video resources:      {total_videos} ({videos_created} new)")
        self.stdout.write(f"Reading resources:    {total_readings} ({readings_created} new)")
        self.stdout.write(f"Total resources:      {total_videos + total_readings}")
        self.stdout.write("──────────────────────────────")
        self.stdout.write("🚀 Run the server: python manage.py runserver")
        self.stdout.write('🔍 Try searching: "Deadlock" or "Binary Tree"')
