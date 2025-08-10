from django.urls import path
from . import views

urlpatterns = [
    path("scrape/", views.scrape_articles, name="scrape_articles"),
]
