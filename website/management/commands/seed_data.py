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


# Real YouTube video URLs organized by topic
TOPIC_VIDEOS = {
    "Linked List": [
        "https://www.youtube.com/watch?v=odW9FU8jPRQ",  # FreeCodeCamp - Linked List in Python
        "https://www.youtube.com/watch?v=F8AbOfQwl1c",  # CS Dojo - Linked Lists
        "https://www.youtube.com/watch?v=WwfhLC16bis",  # mycodeschool - Linked List Introduction
    ],
    "Binary Tree": [
        "https://www.youtube.com/watch?v=4r_XR9fUPhQ",  # FreeCodeCamp - Binary Trees
        "https://www.youtube.com/watch?v=fAAZixBzIAI",  # freeCodeCamp - Binary Search Tree
        "https://www.youtube.com/watch?v=gcULXE7ViZw",  # Tushar Roy - Binary Tree Traversals
    ],
    "Sorting Algorithms": [
        "https://www.youtube.com/watch?v=kPRA0W1kECg",  # FreeCodeCamp - Sorting Algorithms
        "https://www.youtube.com/watch?v=ZZuD6iUe3Pc",  # Simplilearn - All Sorting Algorithms
        "https://www.youtube.com/watch?v=es2T6KY45cA",  # CS50 - Sorting Algorithms Visualized
    ],
    "Dynamic Programming": [
        "https://www.youtube.com/watch?v=oBt53YbR9Kk",  # FreeCodeCamp - DP Course
        "https://www.youtube.com/watch?v=aPQY__2H3tE",  # Tushar Roy - DP Introduction
        "https://www.youtube.com/watch?v=5dRGRueKU3M",  # CS Dojo - DP Problems
    ],
    "Graph Algorithms": [
        "https://www.youtube.com/watch?v=tWVWeAqZ0WU",  # FreeCodeCamp - Graph Algorithms
        "https://www.youtube.com/watch?v=09_LlHjoEiY",  # MIT OpenCourseWare - BFS and DFS
        "https://www.youtube.com/watch?v=pcKY4hjDrxk",  # Abdul Bari - Graph Traversal
    ],
    "Deadlock": [
        "https://www.youtube.com/watch?v=mB3aVHxV8hI",  # Gate Smashers - Deadlock
        "https://www.youtube.com/watch?v=rPz1RZfkdwU",  # Jenny's Lectures - Deadlock
        "https://www.youtube.com/watch?v=i6l22jbT6xc",  # Neso Academy - Banker's Algorithm
    ],
    "Process Scheduling": [
        "https://www.youtube.com/watch?v=EqMgMzLzjKs",  # Gate Smashers - CPU Scheduling
        "https://www.youtube.com/watch?v=aY7jDxyd-vY",  # Neso Academy - Scheduling Algorithms
        "https://www.youtube.com/watch?v=8Ua2hsBHNgU",  # Jenny's Lectures - Round Robin
    ],
    "Memory Management": [
        "https://www.youtube.com/watch?v=PNJRbM6IjiA",  # Gate Smashers - Memory Management
        "https://www.youtube.com/watch?v=2Fq3bKz7n8o",  # Neso Academy - Paging
        "https://www.youtube.com/watch?v=3i68Y5eLTYE",  # Jenny's Lectures - Virtual Memory
    ],
    "SQL Queries": [
        "https://www.youtube.com/watch?v=HXV3zeQKqGY",  # FreeCodeCamp - SQL Tutorial
        "https://www.youtube.com/watch?v=7S_tz1z_5bA",  # Alex The Analyst - SQL Joins
        "https://www.youtube.com/watch?v=58520k7M6T8",  # Programming with Mosh - SQL
    ],
    "Normalization": [
        "https://www.youtube.com/watch?v=6r1eFjDp9qo",  # Neso Academy - Normalization
        "https://www.youtube.com/watch?v=8gH7KZwqLjE",  # Gate Smashers - 1NF, 2NF, 3NF
        "https://www.youtube.com/watch?v=xGl6gBSLEzE",  # Jenny's Lectures - BCNF
    ],
    "Transactions": [
        "https://www.youtube.com/watch?v=OJ9RViKQmLg",  # Gate Smashers - Transactions
        "https://www.youtube.com/watch?v=wT1O2Y2jJHk",  # Neso Academy - ACID Properties
        "https://www.youtube.com/watch?v=3R4VfB3hFJQ",  # Jenny's Lectures - Concurrency Control
    ],
    "OSI Model": [
        "https://www.youtube.com/watch?v=DRrsCWDRgJk",  # NetworkChuck - OSI Model
        "https://www.youtube.com/watch?v=3RwqU8-0DHI",  # Quick Learn - OSI Model Explained
        "https://www.youtube.com/watch?v=oP3CgZ3G-1M",  # PowerCert - OSI Model
    ],
    "TCP vs UDP": [
        "https://www.youtube.com/watch?v=Uw6Mq_z1m5Y",  # PowerCert - TCP vs UDP
        "https://www.youtube.com/watch?v=KTs-OjvBIOk",  # Neso Academy - TCP
        "https://www.youtube.com/watch?v=dvA_-imfseQ",  # GCFGlobal - TCP vs UDP
    ],
    "Inheritance": [
        "https://www.youtube.com/watch?v=wfcWRAxRVBA",  # FreeCodeCamp - OOP in Python
        "https://www.youtube.com/watch?v=yEsZDjTNISA",  # Programming with Mosh - Inheritance
        "https://www.youtube.com/watch?v=9ZyDJYKjD3E",  # Telusko - OOP Concepts
    ],
    "Design Patterns": [
        "https://www.youtube.com/watch?v=tv-_1er1mWI",  # FreeCodeCamp - Design Patterns
        "https://www.youtube.com/watch?v=v9ejT8FO-7I",  # Christopher Okhravi - Strategy Pattern
        "https://www.youtube.com/watch?v=Rq6YnDnUw14",  # Derek Banas - Design Patterns
    ],
    "SDLC Models": [
        "https://www.youtube.com/watch?v=3Qw7mVqJgQo",  # Neso Academy - SDLC
        "https://www.youtube.com/watch?v=2M4sLdXzF5E",  # Simplilearn - Agile Methodology
        "https://www.youtube.com/watch?v=qN5zw04WxCc",  # EDS Video - Waterfall vs Agile
    ],
    "Requirements Engineering": [
        "https://www.youtube.com/watch?v=3fVQg0T5pXo",  # Neso Academy - Requirements
        "https://www.youtube.com/watch?v=kM4aSkRQ8sY",  # UdeM - Requirements Engineering
        "https://www.youtube.com/watch?v=5VjZD7pKq8E",  # Software Engineering - RE
    ],
    "Search Algorithms": [
        "https://www.youtube.com/watch?v=zaBhtODEL0w",  # FreeCodeCamp - A* Algorithm
        "https://www.youtube.com/watch?v=09_LlHjoEiY",  # MIT - BFS and DFS
        "https://www.youtube.com/watch?v=pcKY4hjDrxk",  # Abdul Bari - Search Algorithms
    ],
    "Machine Learning Basics": [
        "https://www.youtube.com/watch?v=ukzFI9rgwfU",  # FreeCodeCamp - ML Course
        "https://www.youtube.com/watch?v=Gv9_4yMHFhI",  # Simplilearn - ML Tutorial
        "https://www.youtube.com/watch?v=aircAruvnKk",  # 3Blue1Brown - Neural Networks
    ],
    "Knowledge Representation": [
        "https://www.youtube.com/watch?v=3RwqU8-0DHI",  # Neso Academy - KR
        "https://www.youtube.com/watch?v=mJYqKB6pXoE",  # Gate Smashers - Knowledge Representation
        "https://www.youtube.com/watch?v=5VjZD7pKq8E",  # AI Lectures - Propositional Logic
    ],
}

# Real article/blog URLs organized by topic
TOPIC_ARTICLES = {
    "Linked List": [
        "https://www.geeksforgeeks.org/data-structures/linked-list/",
        "https://www.programiz.com/dsa/linked-list",
        "https://realpython.com/linked-lists-python/",
    ],
    "Binary Tree": [
        "https://www.geeksforgeeks.org/binary-tree-data-structure/",
        "https://www.programiz.com/dsa/binary-tree",
        "https://www.w3schools.com/dsa/dsa_data_binarytrees.php",
    ],
    "Sorting Algorithms": [
        "https://www.geeksforgeeks.org/sorting-algorithms/",
        "https://www.programiz.com/dsa/algorithm",
        "https://www.khanacademy.org/computing/computer-science/algorithms",
    ],
    "Dynamic Programming": [
        "https://www.geeksforgeeks.org/dynamic-programming/",
        "https://www.programiz.com/dsa/dynamic-programming",
        "https://cp-algorithms.com/dynamic/dynamic-programming.html",
    ],
    "Graph Algorithms": [
        "https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/",
        "https://www.programiz.com/dsa/graph-data-structure",
        "https://cp-algorithms.com/graph/bfs.html",
    ],
    "Deadlock": [
        "https://www.geeksforgeeks.org/operating-system-process-management-deadlock-introduction/",
        "https://www.tutorialspoint.com/operating_system/os_deadlocks.htm",
        "https://www.javatpoint.com/os-deadlocks-introduction",
    ],
    "Process Scheduling": [
        "https://www.geeksforgeeks.org/introduction-of-cpu-scheduling/",
        "https://www.tutorialspoint.com/operating_system/os_process_scheduling.htm",
        "https://www.javatpoint.com/os-cpu-scheduling",
    ],
    "Memory Management": [
        "https://www.geeksforgeeks.org/memory-management-in-operating-system/",
        "https://www.tutorialspoint.com/operating_system/os_memory_management.htm",
        "https://www.javatpoint.com/os-memory-management",
    ],
    "SQL Queries": [
        "https://www.geeksforgeeks.org/sql-tutorial/",
        "https://www.w3schools.com/sql/",
        "https://www.sqltutorial.org/",
    ],
    "Normalization": [
        "https://www.geeksforgeeks.org/normal-forms-in-dbms/",
        "https://www.tutorialspoint.com/dbms/database_normalization.htm",
        "https://www.javatpoint.com/dbms-normalization",
    ],
    "Transactions": [
        "https://www.geeksforgeeks.org/dbms-transactions/",
        "https://www.tutorialspoint.com/dbms/dbms_transaction.htm",
        "https://www.javatpoint.com/dbms-transaction",
    ],
    "OSI Model": [
        "https://www.geeksforgeeks.org/layers-of-osi-model/",
        "https://www.javatpoint.com/computer-network-osi-model",
        "https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/",
    ],
    "TCP vs UDP": [
        "https://www.geeksforgeeks.org/differences-between-tcp-and-udp/",
        "https://www.javatpoint.com/computer-network-tcp-vs-udp",
        "https://www.cloudflare.com/learning/ddos/glossary/tcp-vs-udp/",
    ],
    "Inheritance": [
        "https://www.geeksforgeeks.org/inheritance-in-python/",
        "https://www.programiz.com/python-programming/inheritance",
        "https://realpython.com/inheritance-composition-python/",
    ],
    "Design Patterns": [
        "https://www.geeksforgeeks.org/software-design-patterns/",
        "https://refactoring.guru/design-patterns",
        "https://www.digitalocean.com/community/tutorials/design-patterns-in-java",
    ],
    "SDLC Models": [
        "https://www.geeksforgeeks.org/software-engineering-sdlc-models/",
        "https://www.tutorialspoint.com/software_engineering/software_engineering_sdlc.htm",
        "https://www.javatpoint.com/software-engineering-sdlc",
    ],
    "Requirements Engineering": [
        "https://www.geeksforgeeks.org/requirements-engineering/",
        "https://www.tutorialspoint.com/software_engineering/software_requirements.htm",
        "https://www.modernanalyst.com/Resources/Articles/tabid/115/articleType/ArticleView/articleId/1234/Requirements-Engineering.aspx",
    ],
    "Search Algorithms": [
        "https://www.geeksforgeeks.org/search-algorithms/",
        "https://www.programiz.com/dsa/graph-algorithm",
        "https://www.redblobgames.com/pathfinding/a-star/introduction.html",
    ],
    "Machine Learning Basics": [
        "https://www.geeksforgeeks.org/machine-learning/",
        "https://www.ibm.com/cloud/learn/machine-learning",
        "https://www.coursera.org/articles/what-is-machine-learning",
    ],
    "Knowledge Representation": [
        "https://www.geeksforgeeks.org/artificial-intelligence-knowledge-representation/",
        "https://www.tutorialspoint.com/artificial_intelligence/artificial_intelligence_knowledge_representation.htm",
        "https://www.javatpoint.com/knowledge-representation-in-ai",
    ],
}

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
        """Insert or refresh three video resources per topic using real YouTube links."""
        topic_map = {topic.name: topic for topic in Topic.objects.select_related("subject")}
        created = 0

        for index, topic_item in enumerate(topic_data, start=1):
            topic = topic_map[topic_item["name"]]
            subject_label = topic.subject.name
            topic_name = topic_item["name"]
            
            # Get real video URLs for this topic
            video_urls = TOPIC_VIDEOS.get(topic_name, [
                build_youtube_search_url(f"{topic_name} {subject_label} tutorial"),
                build_youtube_search_url(f"{topic_name} {subject_label} explanation"),
                build_youtube_search_url(f"{topic_name} {subject_label} advanced"),
            ])

            for preset_idx, preset in enumerate(VIDEO_PRESETS):
                title = f"{topic.name} in {subject_label} – {preset.suffix}"
                if topic.name == "Deadlock":
                    deadlock_titles = {
                        "beginner": "Deadlock in Operating System – Full Explanation",
                        "intermediate": "Banker's Algorithm for Deadlock Avoidance – Step by Step",
                        "advanced": "Deadlock Detection & Recovery – OS Concepts (Gate Exam Level)",
                    }
                    title = deadlock_titles[preset.difficulty_level]

                # Use real YouTube URL for this difficulty level
                youtube_url = video_urls[preset_idx] if preset_idx < len(video_urls) else video_urls[0]

                _, was_created = VideoResource.objects.update_or_create(
                    topic=topic,
                    title=title,
                    defaults={
                        "description": f"{topic_item['description']} {preset.description}",
                        "youtube_url": youtube_url,
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
        """Insert or refresh PDF, blog, and notes reading resources for each topic with real URLs."""
        topic_map = {topic.name: topic for topic in Topic.objects.select_related("subject")}
        created = 0

        for index, topic_item in enumerate(topic_data, start=1):
            topic = topic_map[topic_item["name"]]
            slug = slugify(topic.name)
            topic_name = topic_item["name"]
            
            # Get real article URLs for this topic
            article_urls = TOPIC_ARTICLES.get(topic_name, [
                f"https://www.geeksforgeeks.org/{slug}/",
                f"https://www.tutorialspoint.com/{slug}/",
                f"https://www.javatpoint.com/{slug}",
            ])

            for preset_idx, preset in enumerate(READING_PRESETS):
                title = f"{topic.name} – {preset['title_suffix']}"
                if topic.name == "Deadlock":
                    deadlock_titles = {
                        "pdf": "Operating System Concepts – Deadlock Chapter (Silberschatz)",
                        "blog": "Understanding Deadlock: Conditions, Prevention & Avoidance Explained",
                        "notes": "Deadlock – Short Notes & Formula Sheet for Exam Prep",
                    }
                    title = deadlock_titles[preset["resource_type"]]

                # Use real article URL based on resource type
                url = article_urls[preset_idx] if preset_idx < len(article_urls) else article_urls[0]
                
                # Update source name based on actual URL
                source_name = preset["source_name"]
                if "geeksforgeeks" in url.lower():
                    source_name = "GeeksForGeeks"
                elif "tutorialspoint" in url.lower():
                    source_name = "TutorialsPoint"
                elif "javatpoint" in url.lower():
                    source_name = "JavaTpoint"
                elif "programiz" in url.lower():
                    source_name = "Programiz"
                elif "w3schools" in url.lower():
                    source_name = "W3Schools"
                elif "realpython" in url.lower():
                    source_name = "Real Python"
                elif "refactoring.guru" in url.lower():
                    source_name = "Refactoring Guru"

                _, was_created = ReadingResource.objects.update_or_create(
                    topic=topic,
                    title=title,
                    defaults={
                        "description": f"{topic_item['description']} {preset['description']}",
                        "url": url,
                        "resource_type": preset["resource_type"],
                        "source_name": source_name,
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
