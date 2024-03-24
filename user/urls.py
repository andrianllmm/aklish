from django.urls import path
from . import views


app_name = "user"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:user_id>/<str:username>", views.profile, name="profile"),
    # path("profile", views.profile, name="profile"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout")
]