from django.urls import path
from . import views


app_name = "proofread_api"
urlpatterns = [
    path("<str:lang>/", views.proofread, name="proofread")
]