from django.urls import path
from . import views


app_name = "dictionary_api"
urlpatterns = [
    path(
        "<str:lang>/entries/", views.ListDictEntryAPIView.as_view(), name="list_entries"
    ),
    path(
        "<str:lang>/entry/<str:word>/",
        views.RetrieveDictEntryAPIView.as_view(),
        name="retrieve_entry",
    ),
    path(
        "<str:lang>/entry/",
        views.RetrieveDictEntryAPIView.as_view(),
        name="retrieve_entry",
    ),
]
