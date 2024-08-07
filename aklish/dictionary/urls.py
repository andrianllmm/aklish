from django.urls import path

from . import views


app_name = "dictionary"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:lang>/entries/", views.catalog, name="catalog"),
    path("<str:lang>/entries/<str:letter>/", views.catalog, name="catalog"),
    path("<str:lang>/search/", views.search, name="search"),
    path("<str:lang>/entry/<str:word>/", views.entry, name="entry"),
    path(
        "<str:lang>/entry/<str:word>/add_example/<int:attribute_pk>/",
        views.add_example,
        name="add_example",
    ),
    path("<str:lang>/word_of_the_day/", views.word_of_the_day, name="word_of_the_day"),
]
