from django.shortcuts import render


def wordle(request):
    return render(request, "games/wordle.html")
