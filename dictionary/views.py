from django.shortcuts import render, redirect
from .models import PartsOfSpeech, Etymology, Classification, Attribute, DictEntry


def index(request):
    return redirect("dictionary:catalog")


def catalog(request):
    if query := request.GET.get("q"):
        return render(request, "dictionary/catalog.html", {
            "query": query,
            "entries": DictEntry.objects.filter(word__icontains=query),
            "as_definitions": DictEntry.objects.filter(attributes__definition__icontains=query),
        })

    return render(request, "dictionary/catalog.html", {
        "entries": DictEntry.objects.all().extra(select={"lower_word":"lower(word)"}).order_by("lower_word"),
    })


def entry(request, word):
    entry = DictEntry.objects.get(word=word)
    word = entry.word
    attributes = entry.attributes.all()

    return render(request, "dictionary/entry.html", {
        "word": word,
        "attributes": attributes.order_by("pos", "classification"),
    })


def search(request):
    return render(request, "dictionary/search.html")