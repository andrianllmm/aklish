from django.shortcuts import render
from django.contrib.auth.models import User

from translate.models import Entry, Translation
from dictionary.models import DictEntry


def homepage(request):
    return render(
        request,
        "main/homepage.html",
        {
            "entries": Entry.objects.all(),
            "translations": Translation.objects.all(),
            "dict_entries": DictEntry.objects.all(),
            "top_users": User.objects.filter(is_active=True)
            .filter(is_staff=False)
            .order_by("-profile__reputation")[:3],
        },
    )


def about(request):
    return render(request, "main/about.html")


def contact(request):
    return render(request, "main/contact.html")


def sources(request):
    return render(request, "main/sources.html")
