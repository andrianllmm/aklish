from django.urls import path
from . import views


app_name = "games"
urlpatterns = [
    path("wordle/", views.wordle, name="wordle")
]