from django.urls import path
from .views import DefineWordAPIView


app_name = "dictionary_api"
urlpatterns = [
    path("<str:lang>/<str:word>", DefineWordAPIView.as_view(), name="define_word"),
    path("<str:lang>/", DefineWordAPIView.as_view(), name="define_word"),
]
