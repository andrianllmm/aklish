from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import PartsOfSpeech, Origin, Classification, Attribute, DictEntry
from translations.models import Language, Entry


def index(request):
    return redirect("dictionary:catalog", "akl", "a")


def catalog(request, lang, letter=None):
    lang_object = Language.objects.get(code=lang)
    entries = DictEntry.objects.filter(lang=lang_object)

    if letter and letter in "abcdefghijklmnopqrstuvwxyz":
        entries = entries.filter(word__startswith=letter) \
        .extra(select={"lower_word": "lower(word)"}) \
        .order_by("lower_word")

        p = Paginator(entries, 45)
        page = request.GET.get("page") if request.GET.get("page") else 1
        entries = p.get_page(page)

        start = max(1, entries.number - 3)
        end = min(start + 6, entries.paginator.num_pages)
        page_nums = (range(start, end + 1))

        return render(request, "dictionary/catalog.html", {
            "entries": entries,
            "lang": lang_object,
            "current_letter": letter,
            "page_nums": [str(page_num) for page_num in page_nums]
        })
    else:
        entries = entries.order_by("?")[:45]
    
        return render(request, "dictionary/catalog.html", {
            "entries": entries,
            "lang": lang_object,
        })


def search(request, lang):
    if query := request.GET.get("q"):
        lang_object = Language.objects.get(code=lang)
        entries = DictEntry.objects.filter(lang=lang_object) \
        .filter(word__icontains=query) \
        .order_by("word")
        as_definitions = DictEntry.objects.filter(lang=lang_object) \
        .filter(attributes__definition__icontains=query) \
        .order_by("word")

        entries_paginator = Paginator(entries, 30)
        as_definitions_paginator = Paginator(as_definitions, 30)
        page = request.GET.get("page") if request.GET.get("page") else 1
        entries = entries_paginator.get_page(page)
        if int(page) > entries.paginator.num_pages:
            entries = None
        as_definitions = as_definitions_paginator.get_page(page)
        if int(page) > as_definitions.paginator.num_pages:
            as_definitions = None

        start = max(1, entries.number - 3)
        end = min(start + 6, entries.paginator.num_pages)
        page_nums = (range(start, end + 1))

        return render(request, "dictionary/search.html", {
            "query": query,
            "entries": entries,
            "as_definitions": as_definitions,
            "lang": lang_object,
            "page_nums": [str(page_num) for page_num in page_nums]
        })
    else:
        return render(request, "dictionary/search.html")


def entry(request, lang, word):
    lang_object = Language.objects.get(code=lang)
    entry = DictEntry.objects.get(word=word, lang=lang_object)

    return render(request, "dictionary/entry.html", {
        "word": entry.word,
        "attributes": entry.attributes.all().order_by("pos", "classification"),
        "lang": lang_object,
    })


@login_required(login_url="users:login")
def add_example(request, lang, word, attribute_pk):
    lang_object = Language.objects.get(code=lang)
    entry = DictEntry.objects.get(word=word, lang=lang_object)
    attribute = Attribute.objects.get(pk=attribute_pk)

    if request.method == "POST":
        if content := request.POST.get("content"):
            example_entry, created = Entry.objects.get_or_create(
                content=content.strip(),
                lang=lang_object,
                user=request.user,
            )

            attribute.examples.add(example_entry)
        
            return redirect("dictionary:entry", lang, word)

    return render(request, "dictionary/add_example.html", {
        "word": entry.word,
        "attribute": attribute,
        "lang": lang_object,
    })