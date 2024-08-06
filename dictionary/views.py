import datetime
import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Attribute, DictEntry
from translations.models import Language, Entry


def index(request):
    return redirect("dictionary:catalog", "akl", "a")


def catalog(request, lang, letter=None):
    lang_object = get_object_or_404(Language, code=lang)
    entries = DictEntry.objects.filter(lang=lang_object)

    if entries:
        today = datetime.date.today()
        entry_today = entries.filter(last_selected=today).first()

        if not entry_today:
            entry_today = random.choice(entries.all())
            entry_today.last_selected = today
            entry_today.save()
    else:
        entry_today = None

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
            "page_nums": [str(page_num) for page_num in page_nums],
            "entry_today": entry_today,
        })
    else:
        entries = entries.order_by("?")[:45]

        return render(request, "dictionary/catalog.html", {
            "entries": entries,
            "lang": lang_object,
            "entry_today": entry_today,
        })


def search(request, lang):
    if query := request.GET.get("q"):
        lang_object = get_object_or_404(Language, code=lang)
        entries = DictEntry.objects.filter(lang=lang_object)

        if entries:
            today = datetime.date.today()
            entry_today = entries.filter(last_selected=today).first()
            if not entry_today:
                entry_today = random.choice(entries.all())
                entry_today.last_selected = today
                entry_today.save()
        else:
            entry_today = False

        entries = entries.filter(word__icontains=query).order_by("word")
        as_definitions = entries.filter(attributes__definition__icontains=query).order_by("word")

        if query.lower() in ["mnhs", "maloconhs"]:
            entries = DictEntry.objects.filter(Q(word="buot") | Q(word="hugod") | Q(word="aeam"))

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
            "page_nums": [str(page_num) for page_num in page_nums],
            "entry_today": entry_today,
        })
    else:
        return render(request, "dictionary/catalog.html")


@login_required(login_url="users:login")
def entry(request, lang, word):
    lang_object = get_object_or_404(Language, code=lang)
    entry = get_object_or_404(DictEntry, word=word, lang=lang_object)

    return render(request, "dictionary/entry.html", {
        "word": entry.word,
        "attributes": entry.attributes.all().order_by("pos", "classification"),
        "lang": lang_object,
    })


@login_required(login_url="users:login")
def add_example(request, lang, word, attribute_pk):
    lang_object = get_object_or_404(Language, code=lang)
    entry = get_object_or_404(DictEntry, word=word, lang=lang_object)
    attribute = get_object_or_404(Attribute, pk=attribute_pk)

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


def word_of_the_day(request, lang):
    lang_object = get_object_or_404(Language, code=lang)
    entries = DictEntry.objects.filter(lang=lang_object)

    today = datetime.date.today()

    entry = entries.filter(last_selected=today).first()

    if not entry:
        entry = random.choice(entries.all())
        entry.last_selected = today
        entry.save()

    return render(request, "dictionary/entry.html", {
        "word": entry.word,
        "attributes": entry.attributes.all().order_by("pos", "classification"),
        "lang": lang_object,
        "word_of_the_day": True,
    })