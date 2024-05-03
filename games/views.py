from django.shortcuts import render


def wordle(request, lang):
    return render(request, "games/game.html")


def match(request, lang):
    return render(request, "games/game.html")
