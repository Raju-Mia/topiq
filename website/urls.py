"""URL patterns for the website app."""

from django.urls import path

from website import views

app_name = "website"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search_results, name="search_results"),
    path("api/search/", views.api_search, name="api_search"),
    path("api/chat/", views.ai_chat, name="ai_chat"),
    path("bookmark/", views.bookmark_topic, name="bookmark_topic"),
    path("feedback/", views.submit_feedback, name="submit_feedback"),
]
