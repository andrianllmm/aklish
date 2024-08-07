from django.urls import path

from . import views


app_name = "translations"
urlpatterns = [
    path("entries/", views.catalog, name="catalog"),
    path("search/", views.search, name="search"),
    path("entry/<int:entry_id>/", views.entry, name="entry"),
    path("add/", views.add, name="add"),
    path("edit/entry/<int:entry_id>/", views.edit_entry, name="edit_entry"),
    path(
        "edit/translation/<int:translation_id>/",
        views.edit_translation,
        name="edit_translation",
    ),
    path(
        "delete/translation/<int:translation_id>/",
        views.delete_translation,
        name="delete_translation",
    ),
    path("delete/entry/<int:entry_id>/", views.delete_entry, name="delete_entry"),
    path("bookmark/<int:entry_id>/", views.bookmark, name="bookmark"),
    path("vote/<int:translation_id>/", views.vote, name="vote"),
]
