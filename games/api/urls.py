from django.urls import path
from . import views


app_name = "games_api"
urlpatterns = [
    path("stats/", views.GameStatsAPIView.as_view(), name="stats"),
]