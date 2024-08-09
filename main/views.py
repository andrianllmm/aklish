from django.shortcuts import render
from django.contrib.auth.models import User
from django import template

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


def help(request, page=None):
    categories = {
        "Translate": {
            "adding_guide": "Guide in adding entries",
            "translating_guide": "Guide in translating entries",
        },
        "Reputation": {
            "reputation_guide": "What is reputation?",
            "reputation_guide": "How to earn reputation?",
            "reputation_guide": "How reputation is loss?",
        },
        "Proofreader": {
            "proofreader_guide": "How to use proofreader?",
            "proofreader_guide": "How does proofreader works?",
        },
        "Games": {
            "match_guide": "How to play Match?",
            "wordle_guide": "How to play Wordle?",
        },
    }

    default_template = "main/help/index.html"

    if not page:
        return render(request, default_template, {
            "categories": categories,
        })

    page_template = f"main/help/{page}.html"

    try:
        template.loader.get_template(page_template)
        return render(request, page_template)
    except template.TemplateDoesNotExist:
        return render(request, default_template, {
            "categories": categories,
        })
