from django.urls import path

from . import views


app_name = "translate"
urlpatterns = [
    path("entries/", views.catalog, name="catalog"),
    path("entry/<int:entry_pk>/", views.entry, name="entry"),
    path("add/", views.add, name="add"),
    path("edit/entry/<int:entry_pk>/", views.edit_entry, name="edit_entry"),
    path("edit/translation/<int:translation_pk>/", views.edit_translation, name="edit_translation",),
    path("delete/translation/", views.delete_translation, name="delete_translation", ),
    path("delete/entry/", views.delete_entry, name="delete_entry"),
    path("bookmark/<int:entry_pk>/", views.bookmark, name="bookmark"),
    path("vote/<int:translation_pk>/", views.vote, name="vote"),
]
