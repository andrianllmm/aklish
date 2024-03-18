from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

# Create your views here.
def index(request):
    return redirect("user:profile")


@login_required(login_url="user:login")
def profile(request):
    return render(request, "user/profile.html",)


def register(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user:login")

    return render(request, "user/register.html", {
        "register_form": form
    })


def login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                return redirect("translations:homepage")
    return render(request, "user/login.html", {
        "login_form": form
    })


def logout(request):
    auth.logout(request)

    return redirect("translations:homepage")