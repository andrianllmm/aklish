from django.shortcuts import render


def index(request, lang):
    return render(request, "proofreader/index.html")
