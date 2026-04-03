"""ML-powered recommendation engine for Topiq."""

from __future__ import annotations

import logging
import os
import re
import sys
from pathlib import Path
from typing import Any

import django
import numpy as np
from django.db import DatabaseError
from django.db.models import Count, Q

if __name__ == "__main__" and "DJANGO_SETTINGS_MODULE" not in os.environ:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "topiq.settings")
    django.setup()

try:
    from .models import (
        ReadingResource,
        Semester,
        StudentInteraction,
        Subject,
        Topic,
        VideoResource,
    )
except ImportError:  # pragma: no cover - supports direct script execution.
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from website.models import (
        ReadingResource,
        Semester,
        StudentInteraction,
        Subject,
        Topic,
        VideoResource,
    )

logger = logging.getLogger(__name__)

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    SKLEARN_AVAILABLE = True
except ImportError:  # pragma: no cover - exercised only when sklearn is missing.
    TfidfVectorizer = None
    cosine_similarity = None
    SKLEARN_AVAILABLE = False
    logger.warning("scikit-learn is not installed. Falling back to simple string matching.")


class ResourceRecommender:
    """Recommend the best learning resources for a given student query."""

    def __init__(self):
        """Initialize the recommender configuration and vectorizer."""
        self.threshold = 0.15
        self.top_n = 3
        self.vectorizer = (
            TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            if SKLEARN_AVAILABLE and TfidfVectorizer is not None
            else None
        )

    def _empty_result(self, query: str, message: str = "", found: bool = False) -> dict[str, Any]:
        """Return a safe, predictable response shape for failed lookups."""
        return {
            "query": query,
            "matched_topic": None,
            "matched_topic_name": "",
            "subject_name": "",
            "semester_name": "",
            "videos": [],
            "readings": [],
            "similar_topics": [],
            "total_resources": 0,
            "avg_study_time": "0 min",
            "confidence_score": 0.0,
            "found": found,
            "message": message,
        }

    def _normalize_query(self, query: str) -> str:
        """Normalize user input into a consistent searchable string."""
        normalized = re.sub(r"[^a-zA-Z0-9\s]+", " ", query or "")
        normalized = re.sub(r"\s+", " ", normalized).strip().lower()
        return normalized

    def _build_topic_corpus(self) -> list[tuple[int, str]]:
        """Build the text corpus used for TF-IDF topic matching."""
        try:
            topics = (
                Topic.objects.filter(is_active=True, subject__is_active=True, subject__semester__is_active=True)
                .select_related("subject", "subject__semester")
            )
        except DatabaseError as exc:
            logger.exception("Failed to load topics for corpus build: %s", exc)
            return []

        corpus: list[tuple[int, str]] = []
        for topic in topics:
            document = (
                f"{topic.name} "
                f"{topic.subject.name} "
                f"{topic.tags or ''} "
                f"{topic.search_keywords or ''} "
                f"{topic.description or ''}"
            ).strip()
            corpus.append((topic.id, document))

        if not corpus:
            logger.warning("No topics found in database while building TF-IDF corpus.")

        return corpus

    def _simple_search(self, query: str, top_n: int = 5) -> list[tuple[int, float]]:
        """Fallback topic search using case-insensitive database string matching."""
        normalized_query = self._normalize_query(query)
        if not normalized_query:
            return []

        query_tokens = [token for token in normalized_query.split() if token]

        try:
            filters = Q(name__icontains=normalized_query) | Q(tags__icontains=normalized_query)
            for token in query_tokens:
                filters |= Q(name__icontains=token) | Q(tags__icontains=token) | Q(search_keywords__icontains=token)

            topics = (
                Topic.objects.filter(is_active=True)
                .filter(filters)
                .distinct()
                .select_related("subject", "subject__semester")[: top_n * 2]
            )
        except DatabaseError as exc:
            logger.exception("Simple search failed for query '%s': %s", query, exc)
            return []

        results: list[tuple[int, float]] = []
        for topic in topics:
            haystack = self._normalize_query(
                f"{topic.name} {topic.subject.name} {topic.tags or ''} {topic.search_keywords or ''}"
            )
            score = 0.0
            if normalized_query in haystack:
                score += 0.6
            for token in query_tokens:
                if token in haystack:
                    score += 0.15
            if score > 0:
                results.append((topic.id, min(score, 0.99)))

        results.sort(key=lambda item: item[1], reverse=True)
        return results[:top_n]

    def find_matching_topics(self, query: str, top_n: int = 5) -> list[tuple[int, float]]:
        """Return the best matching topic IDs with similarity scores."""
        normalized_query = self._normalize_query(query)
        logger.info("Search query: %s", normalized_query)

        if len(normalized_query) < 2:
            logger.warning("Query too short for topic matching: %s", query)
            return []

        corpus = self._build_topic_corpus()
        if not corpus:
            return []

        if not SKLEARN_AVAILABLE or self.vectorizer is None or cosine_similarity is None:
            return self._simple_search(normalized_query, top_n=top_n)

        topic_ids = [topic_id for topic_id, _ in corpus]
        documents = [document for _, document in corpus]

        try:
            topic_matrix = self.vectorizer.fit_transform(documents)
            query_vector = self.vectorizer.transform([normalized_query])
            similarities = cosine_similarity(query_vector, topic_matrix).flatten()
        except Exception as exc:  # pragma: no cover - defensive fallback.
            logger.exception("TF-IDF search failed. Falling back to simple search: %s", exc)
            return self._simple_search(normalized_query, top_n=top_n)

        ranked_indexes = np.argsort(similarities)[::-1]
        ranked_matches: list[tuple[int, float]] = []

        for index in ranked_indexes:
            score = float(similarities[index])
            if score < self.threshold:
                continue
            ranked_matches.append((topic_ids[index], score))
            if len(ranked_matches) >= top_n:
                break

        if ranked_matches:
            logger.info("Found %s TF-IDF topic matches for query '%s'.", len(ranked_matches), query)
            return ranked_matches

        logger.info("No TF-IDF matches above threshold for '%s'. Trying partial string match.", query)
        return self._simple_search(normalized_query, top_n=top_n)

    def calculate_avg_study_time(self, videos: list[VideoResource]) -> str:
        """Convert video durations into a readable total study time string."""
        total_seconds = 0

        for video in videos:
            if getattr(video, "duration_seconds", 0):
                total_seconds += max(video.duration_seconds, 0)
                continue

            duration = (video.duration or "").strip()
            if not duration:
                continue

            parts = duration.split(":")
            try:
                if len(parts) == 2:
                    minutes, seconds = [int(part) for part in parts]
                    total_seconds += (minutes * 60) + seconds
                elif len(parts) == 3:
                    hours, minutes, seconds = [int(part) for part in parts]
                    total_seconds += (hours * 3600) + (minutes * 60) + seconds
            except ValueError:
                logger.warning("Unable to parse video duration '%s' for video %s", duration, video.pk)

        if total_seconds <= 0:
            return "0 min"

        total_minutes = total_seconds / 60
        if total_minutes < 60:
            return f"{int(round(total_minutes))} min"

        total_hours = total_minutes / 60
        return f"{total_hours:.1f} hrs"

    def get_feedback_score(self, resource_type: str, resource_id: int) -> float:
        """Compute feedback score from interaction data using a safe denominator."""
        try:
            counts = StudentInteraction.objects.filter(
                resource_type=resource_type,
                resource_id=resource_id,
                interaction_type__in=["helpful", "not_helpful"],
            ).aggregate(
                helpful=Count("id", filter=Q(interaction_type="helpful")),
                not_helpful=Count("id", filter=Q(interaction_type="not_helpful")),
            )
        except DatabaseError as exc:
            logger.exception(
                "Failed to calculate feedback score for %s:%s: %s",
                resource_type,
                resource_id,
                exc,
            )
            return 0.0

        helpful = counts.get("helpful", 0) or 0
        not_helpful = counts.get("not_helpful", 0) or 0
        return helpful / (helpful + not_helpful + 1)

    def update_ml_scores(self) -> int:
        """Refresh ML scores for all resources and return the number updated."""
        updated_count = 0

        try:
            for video in VideoResource.objects.all():
                video.student_helpful_count = StudentInteraction.objects.filter(
                    resource_type="video",
                    resource_id=video.id,
                    interaction_type="helpful",
                ).count()
                video.student_not_helpful_count = StudentInteraction.objects.filter(
                    resource_type="video",
                    resource_id=video.id,
                    interaction_type="not_helpful",
                ).count()
                video.calculate_ml_score()
                updated_count += 1

            for reading in ReadingResource.objects.all():
                reading.student_helpful_count = StudentInteraction.objects.filter(
                    resource_type="reading",
                    resource_id=reading.id,
                    interaction_type="helpful",
                ).count()
                reading.student_not_helpful_count = StudentInteraction.objects.filter(
                    resource_type="reading",
                    resource_id=reading.id,
                    interaction_type="not_helpful",
                ).count()
                reading.calculate_ml_score()
                updated_count += 1
        except DatabaseError as exc:
            logger.exception("Failed to update ML scores: %s", exc)
            return updated_count

        logger.info("Updated ML scores for %s resources.", updated_count)
        return updated_count

    def get_recommendations(self, query: str) -> dict[str, Any]:
        """Return the best matched topic and its top-ranked study resources."""
        normalized_query = self._normalize_query(query)
        if len(normalized_query) < 2:
            return self._empty_result(query, message="Query too short", found=False)

        matches = self.find_matching_topics(normalized_query)
        if not matches:
            logger.warning("No topic match found for query '%s'.", query)
            return self._empty_result(query, message="No matching topics found", found=False)

        best_topic_id, confidence_score = matches[0]

        try:
            topic = Topic.objects.select_related("subject", "subject__semester").get(
                pk=best_topic_id,
                is_active=True,
            )
            videos = list(
                VideoResource.objects.filter(topic=topic, is_active=True)
                .select_related("topic")
                .order_by("-ml_score")[: self.top_n]
            )
            readings = list(
                ReadingResource.objects.filter(topic=topic, is_active=True)
                .select_related("topic")
                .order_by("-ml_score")[: self.top_n]
            )
            similar_topics = list(
                Topic.objects.filter(subject=topic.subject, is_active=True)
                .exclude(pk=topic.pk)
                .order_by("name")[:3]
            )
        except DatabaseError as exc:
            logger.exception("Database error while fetching recommendations: %s", exc)
            return self._empty_result(query, message="Database error", found=False)
        except Topic.DoesNotExist:
            logger.warning("Matched topic ID %s no longer exists.", best_topic_id)
            return self._empty_result(query, message="Matched topic not found", found=False)

        matched_topic_name = topic.name
        subject_name = topic.subject.name
        semester_name = topic.subject.semester.name
        total_resources = len(videos) + len(readings)
        avg_study_time = self.calculate_avg_study_time(videos)

        logger.info("Matched topic: %s", topic)
        return {
            "query": topic.full_name,
            "matched_topic": topic,
            "matched_topic_name": matched_topic_name,
            "subject_name": subject_name,
            "semester_name": semester_name,
            "videos": videos,
            "readings": readings,
            "similar_topics": similar_topics,
            "total_resources": total_resources,
            "avg_study_time": avg_study_time,
            "confidence_score": round(float(confidence_score), 2),
            "found": True,
            "message": "",
        }


def search_topics(query: str) -> dict[str, Any]:
    """Search topics using the recommender service and return recommendations."""
    recommender = ResourceRecommender()
    return recommender.get_recommendations(query)


def get_all_semesters():
    """Return all active semesters ordered by their configured display order."""
    try:
        return Semester.objects.filter(is_active=True).order_by("order")
    except DatabaseError as exc:
        logger.exception("Failed to fetch semesters: %s", exc)
        return Semester.objects.none()


def get_subjects_by_semester(semester_id: int):
    """Return active subjects for a specific semester."""
    try:
        return Subject.objects.filter(semester_id=semester_id, is_active=True).order_by("name")
    except DatabaseError as exc:
        logger.exception("Failed to fetch subjects for semester %s: %s", semester_id, exc)
        return Subject.objects.none()


def get_topics_by_subject(subject_id: int):
    """Return active topics for a specific subject."""
    try:
        return Topic.objects.filter(subject_id=subject_id, is_active=True).order_by("name")
    except DatabaseError as exc:
        logger.exception("Failed to fetch topics for subject %s: %s", subject_id, exc)
        return Topic.objects.none()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")

    recommender = ResourceRecommender()
    test_queries = ["deadlock", "binary tree", "sorting algorithm"]

    for query in test_queries:
        result = recommender.get_recommendations(query)
        print(f"\nQuery: {query}")
        print(f"Found: {result['found']}")
        print(f"Matched Topic: {result['matched_topic_name'] or 'None'}")
        print(f"Subject: {result['subject_name'] or 'N/A'}")
        print(f"Semester: {result['semester_name'] or 'N/A'}")
        print(f"Confidence: {result['confidence_score']}")
        print(f"Total Resources: {result['total_resources']}")
        print(f"Average Study Time: {result['avg_study_time']}")
