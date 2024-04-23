from django.urls import path
from . import views


app_name = "proofread_api"
urlpatterns = [
    path("", views.proofread, name="proofread")
]