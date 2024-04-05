from django.urls import path
from . import views


app_name = "spellchecker"
urlpatterns = [
    path("", views.index, name="index")
]