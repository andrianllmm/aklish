from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from translations.models import Language, Entry, Translation
from .forms import RegisterForm, LoginForm


def index(request):
    return render(request, "users/index.html", {
        "users": sorted(User.objects.all(), key=lambda user: user.profile.reputation, reverse=True)
    })


def profile(request, user_id, username):
    if request.method == "POST":
        if request.POST.get("remove_bookmark"):
            entry_to_unbookmark_pk = request.POST.get("entry_to_unbookmark_pk")
            entry_to_unbookmark = Entry.objects.get(pk=entry_to_unbookmark_pk)
            entry_to_unbookmark.bookmarks.remove(request.user)

        if request.POST.get("delete_entry"):
            entry_to_delete_pk = request.POST.get("entry_to_delete_pk")
            entry_to_delete = Entry.objects.get(pk=entry_to_delete_pk)
            entry_to_delete.delete()
        
        if request.POST.get("delete_translation"):
            translation_to_delete_pk = request.POST.get("translation_to_delete_pk")
            translation_to_delete = Translation.objects.get(pk=translation_to_delete_pk)
            translation_to_delete.delete()
        
        return redirect("users:profile", request.user.pk, request.user.username)

    user = User.objects.get(pk=user_id, username=username)
    return render(request, "users/profile.html", {
        "user": user,
    })


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect("users:login")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {
        "form": form
    })


def login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                return redirect("translations:homepage")
    else:
        form = LoginForm()

    return render(request, "users/login.html", {
        "form": form
    })


def logout(request):
    auth.logout(request)

    return redirect("translations:homepage")