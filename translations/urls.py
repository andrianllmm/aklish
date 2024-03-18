from django.urls import path
from . import views


app_name = "translations"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("translations", views.translations, name="translations"),
    path("translations/<int:translation_id>", views.translation_entry, name="translation_entry"),
    path("texts", views.texts, name="texts"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
]