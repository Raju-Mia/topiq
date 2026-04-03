"""Admin registrations for all Topiq database models."""

from django.contrib import admin

from .models import (
    ReadingResource,
    Semester,
    StudentInteraction,
    Subject,
    Topic,
    VideoResource,
)


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    """Admin configuration for semesters."""

    list_display = ("name", "order", "is_active")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin configuration for subjects."""

    list_display = ("name", "semester", "code", "is_active")
    list_filter = ("semester",)
    search_fields = ("name", "code")


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Admin configuration for topics."""

    list_display = ("name", "subject", "slug", "is_active")
    list_filter = ("subject__semester", "subject")
    search_fields = ("name", "tags")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(VideoResource)
class VideoResourceAdmin(admin.ModelAdmin):
    """Admin configuration for video resources."""

    list_display = (
        "title",
        "topic",
        "difficulty_level",
        "rating",
        "view_count",
        "ml_score",
        "is_active",
    )
    list_filter = ("difficulty_level", "topic__subject", "is_active")
    search_fields = ("title",)


@admin.register(ReadingResource)
class ReadingResourceAdmin(admin.ModelAdmin):
    """Admin configuration for reading resources."""

    list_display = ("title", "topic", "resource_type", "rating", "ml_score", "is_active")
    list_filter = ("resource_type", "is_active")
    search_fields = ("title",)


@admin.register(StudentInteraction)
class StudentInteractionAdmin(admin.ModelAdmin):
    """Admin configuration for student interactions."""

    list_display = ("session_key", "topic", "interaction_type", "resource_type", "created_at")
    list_filter = ("interaction_type", "resource_type")
