from django.urls import path

from . import views


app_name = "users"
urlpatterns = [
    path("", views.index, name="index"),
    path("reputation_guide/", views.reputation_guide, name="reputation_guide"),
    path("<int:user_id>/<str:username>/", views.profile, name="profile"),
    path("<int:user_id>/<str:username>/bookmarks_votes/", views.bookmarks_votes, name="bookmarks_votes"),
    path("<int:user_id>/<str:username>/entries_translations/", views.entries_translations, name="entries_translations"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]