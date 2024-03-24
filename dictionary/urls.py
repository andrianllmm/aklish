from django.urls import path
from . import views


app_name = "dictionary"
urlpatterns = [
    path("", views.index, name="index"),
    path("entries", views.catalog, name="catalog"),
    path("entry/<str:word>", views.entry, name="entry"),
    path("search", views.search, name="search")
]