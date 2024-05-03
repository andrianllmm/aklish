from django.urls import path
from . import views


app_name = "games"
urlpatterns = [
    path("wordle/<str:lang>/", views.wordle, name="wordle"),
    path("match/<str:lang>/", views.match, name="match"),
]