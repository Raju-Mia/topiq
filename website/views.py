"""Application views for Topiq."""

from __future__ import annotations

import json
import logging
import os

import requests
from django.contrib import messages
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from website.forms import SearchForm
from website.models import ReadingResource, Semester, StudentInteraction, Topic, VideoResource
from website.recommender import get_all_semesters, search_topics

logger = logging.getLogger(__name__)
DEFAULT_AI_PROVIDER = "groq"
DEFAULT_GROQ_MODEL = "llama-3.1-8b-instant"
DEFAULT_ANTHROPIC_MODEL = "claude-3-5-haiku-latest"


def _ensure_session_key(request) -> str:
    """Ensure the current visitor has a usable session key."""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key or ""


def _get_resource(resource_type: str, resource_id: int):
    """Return the resource instance for the provided type and ID."""
    if resource_type == "video":
        return VideoResource.objects.select_related("topic").get(pk=resource_id)
    if resource_type == "reading":
        return ReadingResource.objects.select_related("topic").get(pk=resource_id)
    raise ValueError("Invalid resource type")


def _get_ai_provider() -> str:
    """Pick the configured AI provider, preferring Groq for local demos."""
    provider = os.environ.get("AI_PROVIDER", "").strip().lower()
    if provider in {"groq", "anthropic"}:
        return provider
    if os.environ.get("GROQ_API_KEY", "").strip():
        return "groq"
    if os.environ.get("ANTHROPIC_API_KEY", "").strip():
        return "anthropic"
    return DEFAULT_AI_PROVIDER


def _call_groq_chat(system_prompt: str, message: str) -> str:
    """Call Groq's chat completions API and return the text reply."""
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing.")

    model_name = os.environ.get("GROQ_MODEL", DEFAULT_GROQ_MODEL).strip() or DEFAULT_GROQ_MODEL
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": model_name,
        "max_tokens": 500,
        "temperature": 0.3,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
    }
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        json=payload,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    response_data = response.json()
    return response_data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()


def _call_anthropic_chat(system_prompt: str, message: str) -> str:
    """Call Anthropic's messages API and return the text reply."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is missing.")

    model_name = os.environ.get("ANTHROPIC_MODEL", DEFAULT_ANTHROPIC_MODEL).strip() or DEFAULT_ANTHROPIC_MODEL
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    payload = {
        "model": model_name,
        "max_tokens": 500,
        "system": system_prompt,
        "messages": [{"role": "user", "content": message}],
    }
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        json=payload,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    response_data = response.json()
    return response_data.get("content", [{}])[0].get("text", "").strip()


# -- VIEW: index --
@require_GET
def index(request):
    """Render the homepage with semester filters and recent search history."""
    try:
        semesters = get_all_semesters()
        recent_searches = request.session.get("recent_searches", [])
        total_resources = VideoResource.objects.filter(is_active=True).count() + ReadingResource.objects.filter(
            is_active=True
        ).count()
        form = SearchForm()

        context = {
            "form": form,
            "query": "",
            "semesters": semesters,
            "recent_searches": recent_searches[-5:],
            "total_resources": total_resources,
            "page_title": "Topiq – Smart Study Resource Finder",
        }
        return render(request, "website/index.html", context)
    except Exception as exc:  # pragma: no cover - defensive error handling.
        logger.exception("Failed to render homepage: %s", exc)
        messages.error(request, "Unable to load the homepage right now. Please try again.")
        context = {
            "form": SearchForm(),
            "query": "",
            "semesters": Semester.objects.none(),
            "recent_searches": [],
            "total_resources": 0,
            "page_title": "Topiq – Smart Study Resource Finder",
        }
        return render(request, "website/index.html", context, status=500)


# -- VIEW: search_results --
@require_GET
def search_results(request):
    """Run the recommender for the search query and render the results page."""
    try:
        query = request.GET.get("q", "").strip()
        semester_id = request.GET.get("semester") or None

        if not query:
            messages.error(request, "Please enter a study topic to search.")
            return redirect("website:index")

        if len(query) < 2:
            messages.error(request, "Please enter at least 2 characters")
            return redirect("website:index")

        cache_key = f"search_{query.lower().replace(' ', '_')}_{semester_id or 'all'}"
        cached_result = cache.get(cache_key)
        if cached_result:
            result = cached_result
        else:
            result = search_topics(query)
            cache.set(cache_key, result, 600)

        recent_searches = request.session.get("recent_searches", [])
        if query in recent_searches:
            recent_searches.remove(query)
        recent_searches.append(query)
        request.session["recent_searches"] = recent_searches[-10:]
        request.session.modified = True

        if result.get("found") and semester_id:
            matched_topic = result.get("matched_topic")
            if matched_topic and str(matched_topic.subject.semester_id) != str(semester_id):
                result = {
                    **result,
                    "found": False,
                    "message": "No matching topic found for the selected semester.",
                    "videos": [],
                    "readings": [],
                    "similar_topics": [],
                    "total_resources": 0,
                }

        bookmarked_topics = request.session.get("bookmarks", [])
        form = SearchForm(initial={"q": query, "semester": semester_id})

        context = {
            "form": form,
            "query": query,
            "result": result,
            "videos": result.get("videos", []),
            "readings": result.get("readings", []),
            "matched_topic": result.get("matched_topic"),
            "similar_topics": result.get("similar_topics", []),
            "avg_study_time": result.get("avg_study_time", ""),
            "semester_name": result.get("semester_name", ""),
            "subject_name": result.get("subject_name", ""),
            "total_resources": result.get("total_resources", 0),
            "confidence_score": result.get("confidence_score", 0),
            "no_results": not result.get("found", False),
            "bookmarked_topics": bookmarked_topics,
            "semesters": get_all_semesters(),
            "page_title": f"{query} – Topiq Results",
        }
        return render(request, "website/results.html", context)
    except Exception as exc:  # pragma: no cover - defensive error handling.
        logger.exception("Search failed: %s", exc)
        messages.error(request, "Something went wrong while searching. Please try again.")
        return redirect("website:index")


# -- VIEW: api_search --
@require_GET
def api_search(request):
    """Return recommendation results as JSON for AJAX-based search."""
    try:
        query = request.GET.get("q", "").strip()
        if not query:
            return JsonResponse({"status": "error", "error": "Empty query"}, status=400)

        result = search_topics(query)
        data = {
            "status": "ok",
            "found": result.get("found", False),
            "query": query,
            "matched_topic_name": result.get("matched_topic_name", ""),
            "subject_name": result.get("subject_name", ""),
            "semester_name": result.get("semester_name", ""),
            "videos": [
                {
                    "id": video.id,
                    "title": video.title,
                    "description": video.description,
                    "youtube_url": video.youtube_url,
                    "thumbnail_url": video.thumbnail_url,
                    "duration": video.duration,
                    "difficulty_level": video.difficulty_level,
                    "rating": video.rating,
                }
                for video in result.get("videos", [])
            ],
            "readings": [
                {
                    "id": reading.id,
                    "title": reading.title,
                    "description": reading.description,
                    "url": reading.url,
                    "resource_type": reading.resource_type,
                    "source_name": reading.source_name,
                    "rating": reading.rating,
                }
                for reading in result.get("readings", [])
            ],
            "total_resources": result.get("total_resources", 0),
            "avg_study_time": result.get("avg_study_time", ""),
            "message": result.get("message", ""),
        }
        return JsonResponse(data)
    except Exception as exc:  # pragma: no cover - defensive error handling.
        logger.exception("API search failed: %s", exc)
        return JsonResponse(
            {"status": "error", "error": "Unable to process search right now."},
            status=500,
        )


# -- VIEW: ai_chat --
@require_POST
def ai_chat(request):
    """Send an academic question to the configured LLM provider and return the reply."""
    try:
        body = json.loads(request.body or "{}")
        message = body.get("message", "").strip()
        topic_context = body.get("topic_context", "").strip()

        if not message:
            return JsonResponse({"status": "error", "error": "Empty message"}, status=400)

        system_prompt = (
            "You are an academic study assistant for university students using the Topiq platform. "
            "You ONLY answer university-level academic questions related to computer science, "
            "engineering, and related subjects. "
            f"If asked about {topic_context or 'the current study topic'}, give a clear, educational explanation. "
            "Do NOT answer questions about personal advice, politics, entertainment, or anything non-academic. "
            "If a non-academic question is asked, politely decline and ask for an academic question. "
            "Keep answers concise, clear, and student-friendly. Use bullet points and examples when helpful."
        )

        provider = _get_ai_provider()
        if provider == "groq" and not os.environ.get("GROQ_API_KEY", "").strip():
            logger.warning("Groq API key is missing.")
            return JsonResponse(
                {
                    "status": "error",
                    "reply": "Sorry, I am temporarily unavailable. Please add GROQ_API_KEY and try again later.",
                },
            )

        if provider == "anthropic" and not os.environ.get("ANTHROPIC_API_KEY", "").strip():
            logger.warning("Anthropic API key is missing.")
            return JsonResponse(
                {
                    "status": "error",
                    "reply": "Sorry, I am temporarily unavailable. Please add ANTHROPIC_API_KEY and try again later.",
                },
            )

        if provider == "groq":
            model_name = os.environ.get("GROQ_MODEL", DEFAULT_GROQ_MODEL).strip() or DEFAULT_GROQ_MODEL
            ai_reply = _call_groq_chat(system_prompt, message)
        else:
            model_name = os.environ.get("ANTHROPIC_MODEL", DEFAULT_ANTHROPIC_MODEL).strip() or DEFAULT_ANTHROPIC_MODEL
            ai_reply = _call_anthropic_chat(system_prompt, message)

        if not ai_reply:
            logger.warning("%s API returned an empty reply.", provider.title())
            ai_reply = "I could not generate an answer right now. Please ask another academic question."

        return JsonResponse({"status": "ok", "reply": ai_reply})
    except json.JSONDecodeError:
        logger.warning("Invalid JSON payload received for AI chat.")
        return JsonResponse({"status": "error", "error": "Invalid JSON body"}, status=400)
    except requests.RequestException as exc:
        response = getattr(exc, "response", None)
        error_detail = ""
        if response is not None:
            try:
                error_payload = response.json()
                error_detail = error_payload.get("error", {}).get("message", "") or response.text
            except ValueError:
                error_detail = response.text

        logger.exception(
            "%s API request failed for model '%s': %s | detail=%s",
            locals().get("provider", _get_ai_provider()).title(),
            locals().get("model_name", DEFAULT_ANTHROPIC_MODEL),
            exc,
            error_detail,
        )

        reply = "Sorry, I am temporarily unavailable. Please try again later."
        if error_detail:
            detail_lower = error_detail.lower()
            provider = locals().get("provider", _get_ai_provider())
            if "model" in detail_lower:
                reply = (
                    "AI chat is misconfigured for the current model. "
                    f"Set {'GROQ_MODEL' if provider == 'groq' else 'ANTHROPIC_MODEL'} in .env to a model your API key can access."
                )
            elif "credit balance is too low" in detail_lower or "purchase credits" in detail_lower:
                reply = f"{provider.title()} API credits are exhausted for this key. Please add billing or purchase credits."
            elif "api key" in detail_lower or "authentication" in detail_lower or "unauthorized" in detail_lower:
                reply = (
                    "API key is invalid or missing permission. "
                    f"Please check {'GROQ_API_KEY' if provider == 'groq' else 'ANTHROPIC_API_KEY'}."
                )

        return JsonResponse(
            {
                "status": "error",
                "reply": reply,
            },
        )
    except Exception as exc:  # pragma: no cover - defensive error handling.
        logger.exception("AI chat failed: %s", exc)
        return JsonResponse(
            {"status": "error", "error": "Unable to process your message right now."},
            status=500,
        )


# -- VIEW: bookmark_topic --
@require_POST
def bookmark_topic(request):
    """Add or remove a topic bookmark for the current session."""
    try:
        body = json.loads(request.body or "{}")
        topic_id = body.get("topic_id")
        if not topic_id:
            return JsonResponse({"status": "error", "error": "topic_id is required"}, status=400)

        topic = get_object_or_404(Topic, pk=topic_id, is_active=True)
        session_key = _ensure_session_key(request)

        bookmarks = request.session.get("bookmarks", [])
        topic_id_str = str(topic.id)

        if topic_id_str in [str(bookmark) for bookmark in bookmarks]:
            bookmarks = [bookmark for bookmark in bookmarks if str(bookmark) != topic_id_str]
            StudentInteraction.objects.filter(
                session_key=session_key,
                topic=topic,
                resource_type="reading",
                resource_id=topic.id,
                interaction_type="bookmark",
            ).delete()
            action = "removed"
        else:
            bookmarks.append(topic.id)
            StudentInteraction.objects.get_or_create(
                session_key=session_key,
                topic=topic,
                resource_type="reading",
                resource_id=topic.id,
                interaction_type="bookmark",
            )
            action = "added"

        request.session["bookmarks"] = bookmarks
        request.session.modified = True

        return JsonResponse(
            {
                "status": "ok",
                "action": action,
                "topic_id": topic.id,
                "topic_name": topic.name,
                "bookmark_count": len(bookmarks),
            }
        )
    except json.JSONDecodeError:
        logger.warning("Invalid JSON payload received for bookmark request.")
        return JsonResponse({"status": "error", "error": "Invalid JSON body"}, status=400)
    except Topic.DoesNotExist:
        logger.warning("Bookmark requested for missing topic.")
        return JsonResponse({"status": "error", "error": "Topic not found"}, status=404)
    except Exception as exc:  # pragma: no cover - defensive error handling.
        logger.exception("Bookmark toggle failed: %s", exc)
        return JsonResponse(
            {"status": "error", "error": "Unable to update bookmark right now."},
            status=500,
        )


# -- VIEW: submit_feedback --
@require_POST
def submit_feedback(request):
    """Store helpful or not-helpful feedback and refresh resource scoring."""
    try:
        body = json.loads(request.body or "{}")
        resource_type = body.get("resource_type", "").strip()
        resource_id = body.get("resource_id")
        feedback_type = body.get("feedback_type", "").strip()
        topic_id = body.get("topic_id")

        if resource_type not in {"video", "reading"}:
            return JsonResponse({"status": "error", "error": "Invalid resource_type"}, status=400)
        if feedback_type not in {"helpful", "not_helpful"}:
            return JsonResponse({"status": "error", "error": "Invalid feedback_type"}, status=400)
        if not resource_id or not topic_id:
            return JsonResponse(
                {"status": "error", "error": "resource_id and topic_id are required"},
                status=400,
            )

        session_key = _ensure_session_key(request)
        topic = get_object_or_404(Topic, pk=topic_id)
        resource = _get_resource(resource_type, int(resource_id))

        existing_interactions = StudentInteraction.objects.filter(
            session_key=session_key,
            topic=topic,
            resource_type=resource_type,
            resource_id=resource.id,
            interaction_type__in=["helpful", "not_helpful"],
        )

        previous_interaction = existing_interactions.first()

        if previous_interaction is None:
            StudentInteraction.objects.create(
                session_key=session_key,
                topic=topic,
                resource_type=resource_type,
                resource_id=resource.id,
                interaction_type=feedback_type,
            )
            if feedback_type == "helpful":
                resource.student_helpful_count += 1
            else:
                resource.student_not_helpful_count += 1
        elif previous_interaction.interaction_type != feedback_type:
            if previous_interaction.interaction_type == "helpful":
                resource.student_helpful_count = max(resource.student_helpful_count - 1, 0)
            else:
                resource.student_not_helpful_count = max(resource.student_not_helpful_count - 1, 0)

            previous_interaction.interaction_type = feedback_type
            previous_interaction.save(update_fields=["interaction_type"])

            if feedback_type == "helpful":
                resource.student_helpful_count += 1
            else:
                resource.student_not_helpful_count += 1

        resource.save(
            update_fields=[
                "student_helpful_count",
                "student_not_helpful_count",
                "ml_score",
                "updated_at",
                *(
                    ["youtube_video_id", "thumbnail_url"]
                    if resource_type == "video"
                    else []
                ),
            ]
        )

        return JsonResponse(
            {
                "status": "ok",
                "feedback": feedback_type,
                "resource_id": resource.id,
                "helpful_count": resource.student_helpful_count,
                "not_helpful_count": resource.student_not_helpful_count,
            }
        )
    except json.JSONDecodeError:
        logger.warning("Invalid JSON payload received for feedback request.")
        return JsonResponse({"status": "error", "error": "Invalid JSON body"}, status=400)
    except (Topic.DoesNotExist, VideoResource.DoesNotExist, ReadingResource.DoesNotExist):
        logger.warning("Feedback requested for missing topic or resource.")
        return JsonResponse({"status": "error", "error": "Resource not found"}, status=404)
    except ValueError as exc:
        logger.warning("Feedback validation failed: %s", exc)
        return JsonResponse({"status": "error", "error": str(exc)}, status=400)
    except Exception as exc:  # pragma: no cover - defensive error handling.
        logger.exception("Feedback submission failed: %s", exc)
        return JsonResponse(
            {"status": "error", "error": "Unable to submit feedback right now."},
            status=500,
        )
