from django.urls import path

from . import views

urlpatterns = [
    path("portfolio/", views.portfolio_payload, name="portfolio-payload"),
    path("track/", views.track_visit, name="track-visit"),
    path("contact/", views.contact, name="contact"),
    path("stats/", views.stats, name="stats"),
    path("stats/login/", views.stats_login, name="stats-login"),
    path("stats/logout/", views.stats_logout, name="stats-logout"),
    path("stats/me/", views.stats_me, name="stats-me"),
]
