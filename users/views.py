from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone

from .models import LoginSession
from translations.models import Entry, Translation, Vote
from .forms import RegisterForm, LoginForm


def index(request):
    return render(request, "users/index.html", {
        "users": User.objects.order_by("-profile__reputation", "date_joined").filter(is_active=True).filter(is_staff=False)
    })


def reputation_guide(request):
    return render(request, "users/reputation_guide.html")


def profile(request, user_id, username):
    user = get_object_or_404(User, pk=user_id, username=username)
    return render(request, "users/profile.html", {
        "user": user,
    })


def bookmarks_votes(request, user_id, username):
    if request.method == "POST":
        if request.POST.get("remove_bookmark"):
            entry_to_unbookmark_pk = request.POST.get("entry_to_unbookmark_pk")
            entry_to_unbookmark = get_object_or_404(Entry, pk=entry_to_unbookmark_pk)
            entry_to_unbookmark.bookmarks.remove(request.user)

        if request.POST.get("remove_vote"):
            vote_to_unvote_pk = request.POST.get("vote_to_unvote_pk")
            vote_to_unvote = get_object_or_404(Vote, pk=vote_to_unvote_pk)
            vote_to_unvote.delete()

        return redirect("users:bookmarks_votes", request.user.pk, request.user.username)

    user = get_object_or_404(User, pk=user_id, username=username)
    return render(request, "users/bookmarks_votes.html", {
        "user": user,
    })


def entries_translations(request, user_id, username):
    if request.method == "POST":
        if request.POST.get("delete_entry"):
            entry_to_delete_pk = request.POST.get("entry_to_delete_pk")
            entry_to_delete = get_object_or_404(Entry, pk=entry_to_delete_pk)
            entry_to_delete.delete()

        if request.POST.get("delete_translation"):
            translation_to_delete_pk = request.POST.get("translation_to_delete_pk")
            translation_to_delete = get_object_or_404(Translation, pk=translation_to_delete_pk)
            translation_to_delete.delete()

        return redirect("users:entries_translations", request.user.pk, request.user.username)

    user = get_object_or_404(User, pk=user_id, username=username)
    return render(request, "users/entries_translations.html", {
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

    return render(request, "users/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                user.profile.login_count += 1
                user.profile.save()

                LoginSession.objects.create(
                    user=user,
                    login_at=timezone.now(),
                )

                next_page = request.GET.get("next", "/")
                return redirect(next_page)
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


def logout(request):
    if request.user.is_authenticated:
        last_login_session = LoginSession.objects.filter(user=request.user, logout_at=None).order_by("-login_at").first()
        if last_login_session:
            last_login_session.logout_at = timezone.now()
            last_login_session.save()

    auth.logout(request)

    return redirect("main:homepage")