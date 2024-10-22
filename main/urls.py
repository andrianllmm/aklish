from django.urls import path

from . import views


app_name = "main"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("sources/", views.sources, name="sources"),
    path("help/", views.help, name="help"),
    path("help/<str:page>/", views.help, name="help"),
]
