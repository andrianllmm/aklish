from django.urls import path
from . import views


app_name = "dictionary_api"
urlpatterns = [
    path("<str:lang>/<str:word>", views.define_word, name="define_word"),
    path("<str:lang>/", views.define_word, name="define_word"),
]