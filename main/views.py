from django.shortcuts import render
from translations.models import Entry, Translation
from dictionary.models import DictEntry
from django.contrib.auth.models import User


def homepage(request):
    return render(request, "main/homepage.html", {
        "entries": Entry.objects.all(),
        "translations": Translation.objects.all(),
        "dict_entries": DictEntry.objects.all(),
        "top_users": User.objects.order_by("-profile__reputation")[:3]
    })


def about(request):
    return render(request, "main/about.html")


def sources(request):
    return render(request, "main/sources.html")
