from django.shortcuts import render


def wordle(request, lang):
    return render(request, "games/wordle.html")
