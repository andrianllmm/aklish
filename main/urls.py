from django.urls import path
from . import views


app_name = "main"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("about/", views.about, name="about"),
    path("sources/", views.sources, name="sources"),
]