from django.urls import path
from . import views


app_name = "translations"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("entries", views.catalog, name="catalog"),
    path("entries/<int:entry_id>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
]