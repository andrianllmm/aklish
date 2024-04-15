from django.urls import path
from . import views


app_name = "proofreader"
urlpatterns = [
    path("", views.index, name="index")
]