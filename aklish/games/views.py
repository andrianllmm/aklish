from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def wordle(request, lang):
    return render(request, "games/wordle.html")


@login_required
def match(request, lang):
    return render(request, "games/match.html")
