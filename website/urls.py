"""URL patterns for the website app."""

from django.urls import path

from .views import home


urlpatterns = [
    path("", home, name="home"),
]
