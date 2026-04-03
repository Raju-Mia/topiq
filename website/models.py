"""Database models for the Topiq recommendation system."""

from __future__ import annotations

import re
from urllib.parse import parse_qs, urlparse

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class Semester(models.Model):
    """Represents an academic semester in the university curriculum."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    order = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Model metadata for sorting and admin display."""

        ordering = ["order"]

    def __str__(self) -> str:
        """Return the semester name for readable admin labels."""
        return self.name


class Subject(models.Model):
    """Represents a subject that belongs to a specific semester."""

    id = models.AutoField(primary_key=True)
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name="subjects",
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Model metadata for consistent subject ordering."""

        ordering = ["semester", "name"]

    def __str__(self) -> str:
        """Return a human-friendly subject label with semester context."""
        return f"{self.name} ({self.semester.name})"


class Topic(models.Model):
    """Represents a searchable topic under a subject."""

    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="topics",
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=300, blank=True, null=True)
    search_keywords = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Model metadata for alphabetical topic ordering."""

        ordering = ["name"]

    def __str__(self) -> str:
        """Return the subject-topic label shown across the application."""
        return f"{self.subject.name} – {self.name}"

    @property
    def full_name(self) -> str:
        """Return the full subject and topic name for display purposes."""
        return f"{self.subject.name} – {self.name}"

    @property
    def tag_list(self) -> list[str]:
        """Return a cleaned list of tags for search and template use."""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]

    def _generate_unique_slug(self) -> str:
        """Generate a unique slug based on the topic name."""
        base_slug = slugify(self.name) or "topic"
        slug = base_slug
        suffix = 1

        while Topic.objects.exclude(pk=self.pk).filter(slug=slug).exists():
            suffix += 1
            slug = f"{base_slug}-{suffix}"

        return slug

    def save(self, *args, **kwargs):
        """Auto-generate a unique slug before saving the topic."""
        if not self.slug:
            self.slug = self._generate_unique_slug()
        elif Topic.objects.exclude(pk=self.pk).filter(slug=self.slug).exists():
            self.slug = self._generate_unique_slug()

        super().save(*args, **kwargs)


class VideoResource(models.Model):
    """Stores a recommended YouTube video resource for a topic."""

    DIFFICULTY_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="videos",
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    youtube_url = models.URLField()
    youtube_video_id = models.CharField(max_length=20, blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    duration = models.CharField(max_length=10)
    duration_seconds = models.IntegerField(default=0)
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default="beginner",
    )
    view_count = models.IntegerField(default=0)
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )
    student_helpful_count = models.IntegerField(default=0)
    student_not_helpful_count = models.IntegerField(default=0)
    ml_score = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Model metadata for ranking videos by recommendation score."""

        ordering = ["-ml_score"]

    def __str__(self) -> str:
        """Return the resource title for admin and template display."""
        return self.title

    @staticmethod
    def extract_youtube_video_id(youtube_url: str) -> str:
        """Extract the YouTube video ID from common YouTube URL formats."""
        if not youtube_url:
            return ""

        parsed = urlparse(youtube_url)
        hostname = parsed.netloc.lower()

        if "youtu.be" in hostname:
            return parsed.path.strip("/").split("/")[0]

        if "youtube.com" in hostname:
            if parsed.path == "/watch":
                return parse_qs(parsed.query).get("v", [""])[0]
            if parsed.path.startswith(("/embed/", "/shorts/", "/live/")):
                match = re.search(r"^/(?:embed|shorts|live)/([^/?&]+)", parsed.path)
                if match:
                    return match.group(1)

        match = re.search(
            r"(?:v=|/embed/|youtu\.be/|/shorts/|/live/)([A-Za-z0-9_-]{6,20})",
            youtube_url,
        )
        return match.group(1) if match else ""

    @property
    def feedback_score(self) -> float:
        """Return the helpful feedback ratio with safe zero-division handling."""
        total_feedback = self.student_helpful_count + self.student_not_helpful_count
        if total_feedback == 0:
            return 0.0
        return self.student_helpful_count / total_feedback

    @property
    def difficulty_color(self) -> str:
        """Return a CSS-friendly color label for the difficulty badge."""
        color_map = {
            "beginner": "green",
            "intermediate": "orange",
            "advanced": "red",
        }
        return color_map.get(self.difficulty_level, "green")

    def build_thumbnail_url(self) -> str:
        """Build the standard YouTube thumbnail URL from the video ID."""
        if not self.youtube_video_id:
            return ""
        return f"https://img.youtube.com/vi/{self.youtube_video_id}/hqdefault.jpg"

    def calculate_ml_score(self, commit: bool = True) -> float:
        """Calculate and optionally persist the machine-learning ranking score."""
        normalized_views = self.view_count / 1_000_000
        self.ml_score = (self.rating * 0.4) + (normalized_views * 0.3) + (
            self.feedback_score * 0.3
        )
        if commit and self.pk:
            self.save(update_fields=["ml_score", "updated_at"])
        return self.ml_score

    def save(self, *args, **kwargs):
        """Extract YouTube metadata and refresh the ML score before saving."""
        self.youtube_video_id = self.extract_youtube_video_id(self.youtube_url) or None
        self.thumbnail_url = self.build_thumbnail_url() or None
        self.ml_score = self.calculate_ml_score(commit=False)
        super().save(*args, **kwargs)


class ReadingResource(models.Model):
    """Stores a recommended reading resource for a topic."""

    TYPE_CHOICES = [
        ("pdf", "PDF Textbook"),
        ("blog", "Blog Article"),
        ("notes", "Study Notes"),
        ("article", "Article"),
    ]

    id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="readings",
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    source_name = models.CharField(max_length=100, blank=True, null=True)
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )
    view_count = models.IntegerField(default=0)
    student_helpful_count = models.IntegerField(default=0)
    student_not_helpful_count = models.IntegerField(default=0)
    ml_score = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Model metadata for ranking readings by recommendation score."""

        ordering = ["-ml_score"]

    def __str__(self) -> str:
        """Return a readable label showing the title and resource type."""
        return f"{self.title} ({self.resource_type})"

    @property
    def feedback_score(self) -> float:
        """Return the helpful feedback ratio with safe zero-division handling."""
        total_feedback = self.student_helpful_count + self.student_not_helpful_count
        if total_feedback == 0:
            return 0.0
        return self.student_helpful_count / total_feedback

    @property
    def type_icon(self) -> str:
        """Return a lightweight icon identifier for the resource type."""
        icon_map = {
            "pdf": "file-text",
            "blog": "globe",
            "notes": "sticky-note",
            "article": "book-open",
        }
        return icon_map.get(self.resource_type, "file")

    @property
    def type_color(self) -> str:
        """Return a CSS-friendly color label for the resource type."""
        color_map = {
            "pdf": "red",
            "blog": "purple",
            "notes": "green",
            "article": "blue",
        }
        return color_map.get(self.resource_type, "gray")

    def calculate_ml_score(self, commit: bool = True) -> float:
        """Calculate and optionally persist the machine-learning ranking score."""
        normalized_views = self.view_count / 1_000_000
        self.ml_score = (self.rating * 0.4) + (normalized_views * 0.3) + (
            self.feedback_score * 0.3
        )
        if commit and self.pk:
            self.save(update_fields=["ml_score", "updated_at"])
        return self.ml_score

    def save(self, *args, **kwargs):
        """Refresh the ML score before saving the reading resource."""
        self.ml_score = self.calculate_ml_score(commit=False)
        super().save(*args, **kwargs)


class StudentInteraction(models.Model):
    """Tracks anonymous student actions using the Django session key."""

    RESOURCE_TYPE_CHOICES = [
        ("video", "Video"),
        ("reading", "Reading"),
    ]

    INTERACTION_CHOICES = [
        ("bookmark", "Bookmark"),
        ("helpful", "Helpful"),
        ("not_helpful", "Not Helpful"),
        ("view", "Viewed"),
    ]

    id = models.AutoField(primary_key=True)
    session_key = models.CharField(max_length=40)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="interactions",
    )
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    resource_id = models.IntegerField()
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Model metadata for uniqueness and reverse chronological ordering."""

        unique_together = [
            ("session_key", "topic", "resource_type", "resource_id", "interaction_type")
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """Return a readable label describing the stored student action."""
        return (
            f"Session {self.session_key[:8]}... → "
            f"{self.interaction_type} on {self.topic.name}"
        )
