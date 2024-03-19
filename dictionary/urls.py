from django.urls import path
from . import views


app_name = "dictionary"
urlpatterns = [
    path("", views.index, name="index"),
    path("catalog", views.catalog, name="catalog"),
    path("<int:entry_id>", views.entry, name="entry"),
    path("search", views.search, name="search")
]