from django.shortcuts import render, redirect
from .models import DictEntry

# Create your views here.
def index(request):
    return redirect("dictionary:catalog")


def catalog(request):
    if query := request.GET.get("q"):
        return render(request, "dictionary/catalog.html", {
        "entries": DictEntry.objects.filter(word__contains=query)
        })

    return render(request, "dictionary/catalog.html", {
        "entries": DictEntry.objects.all(),
    })


def entry(request, entry_id):
    entry = DictEntry.objects.get(pk=entry_id)
    word = entry.word
    definitions = entry.definition.split("; ")
    return render(request, "dictionary/entry.html", {
        "word": word,
        "definitions": definitions
    })


def search(request):
    return render(request, "dictionary/search.html")