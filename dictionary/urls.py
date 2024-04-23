from django.urls import path
from . import views


app_name = "dictionary"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:lang>/entries/", views.catalog, name="catalog"),
    path("<str:lang>/entries/<str:letter>/", views.catalog, name="catalog"),
    path("<str:lang>/search/", views.search, name="search"),
    path("<str:lang>/entry/<str:word>/", views.entry, name="entry"),
]