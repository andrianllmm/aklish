from django.shortcuts import render, redirect
from .models import PartsOfSpeech, Origin, Classification, Attribute, DictEntry
from translations.models import Language


def index(request):
    return redirect("dictionary:catalog", "akl")


def catalog(request, lang):
    lang_object = Language.objects.get(code=lang)
    dict_entries = DictEntry.objects.filter(lang=lang_object)

    if query := request.GET.get("q"):
        return render(request, "dictionary/catalog.html", {
            "query": query,
            "entries": dict_entries.filter(word__icontains=query),
            "as_definitions": dict_entries.filter(attributes__definition__icontains=query),
            "lang": lang_object,
        })

    return render(request, "dictionary/catalog.html", {
        "entries": dict_entries
        .extra(select={"lower_word": "lower(word)"})
        .order_by("lower_word"),
        "lang": lang_object,
    })


def entry(request, lang, word):
    lang_object = Language.objects.get(code=lang)
    dict_entries = DictEntry.objects.filter(lang=lang_object)

    entry = dict_entries.get(word=word)

    return render(request, "dictionary/entry.html", {
        "word": entry.word,
        "attributes": entry.attributes.all().order_by("pos", "classification"),
        "lang": lang_object,
    })