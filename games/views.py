from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url="users:login")
def wordle(request, lang):
    return render(request, "games/game.html")


@login_required(login_url="users:login")
def match(request, lang):
    return render(request, "games/game.html")
