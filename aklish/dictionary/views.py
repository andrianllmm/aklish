from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .models import Attribute, DictEntry
from translate.models import Language, Entry

from .helpers import get_word_today


def index(request):
    return redirect("dictionary:catalog", "akl", "a")


def catalog(request, lang, letter=None):
    lang_object = get_object_or_404(Language, code=lang)
    entries = DictEntry.objects.filter(lang=lang_object)

    # Get word of the day
    entry_today = get_word_today(entries)

    # Letter must be a letter or None
    if letter and letter not in "abcdefghijklmnopqrstuvwxyz":
        letter = None

    # Filter entries with letter
    if letter:
        entries = entries.filter(word__startswith=letter)

    # Order entries case-insensitively
    entries = entries.extra(select={"lower_word": "lower(word)"}).order_by("lower_word")

    page = request.GET.get("page") if request.GET.get("page") else 1
    num_entries_to_show = 20

    # Initialize as_translations and filter entries if query exists
    if query := request.GET.get("q"):
        num_entries_to_show = num_entries_to_show / 2

        entries = entries.filter(word__icontains=query)
        as_definitions = entries.filter(attributes__definition__icontains=query)

        # as_definitions pagination
        as_definitions_paginator = Paginator(as_definitions, num_entries_to_show)

        as_definitions_paginated = as_definitions_paginator.get_page(page)
        if int(page) > as_definitions_paginated.paginator.num_pages:
            as_definitions_paginated = None
    else:
        as_definitions_paginated = None

    # entries pagination
    entries_paginator = Paginator(entries, num_entries_to_show)

    entries_paginated = entries_paginator.get_page(page)
    if int(page) > entries_paginated.paginator.num_pages:
        entries_paginated = None

    # Calculate range of page numbers to show
    page_nums_to_show = 6
    start = int(max(1, entries_paginated.number - (page_nums_to_show / 2)))
    end = int(min(start + page_nums_to_show, entries_paginated.paginator.num_pages))
    page_nums = range(start, end + 1)

    return render(request, "dictionary/catalog.html", {
        "query": query or "",
        "entries": entries_paginated,
        "as_definitions": as_definitions_paginated,
        "lang": lang_object,
        "current_letter": letter,
        "page_nums": [str(page_num) for page_num in page_nums],
        "entry_today": entry_today,
    })


@login_required
def entry(request, lang, word):
    lang_object = get_object_or_404(Language, code=lang)
    entry = get_object_or_404(DictEntry, word=word, lang=lang_object)

    return render(request, "dictionary/entry.html", {
        "word": entry.word,
        "attributes": entry.attributes.all().order_by("pos", "classification"),
        "lang": lang_object,
    })


@login_required
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

    entry = get_word_today(entries)

    return render(request, "dictionary/entry.html", {
        "word": entry.word,
        "attributes": entry.attributes.all().order_by("pos", "classification"),
        "lang": lang_object,
        "word_of_the_day": True,
    })