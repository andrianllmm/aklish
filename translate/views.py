from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Language, Entry, Translation, Vote

from .helpers import sort_entries


def catalog(request):
    entries = Entry.objects.filter(user__is_active=True)

    # Sort entries
    sort_by = request.GET.get("sort", "latest")
    entries = sort_entries(entries, sort_by)

    # Initialize page number and number of entries to show
    page = request.GET.get("page") if request.GET.get("page") else 1
    num_entries_to_show = 10

    # Initialize as_translations and filter entries if query exists
    if query := request.GET.get("q"):
        num_entries_to_show = num_entries_to_show / 2

        entries = entries.filter(content__icontains=query)
        as_translations = entries.filter(translations__content__icontains=query)

        # as_translations pagination
        as_translations_paginator = Paginator(as_translations, num_entries_to_show)

        as_translations_paginated = as_translations_paginator.get_page(page)
        if int(page) > as_translations_paginated.paginator.num_pages:
            as_translations_paginated = None
    else:
        as_translations_paginated = None

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

    return render(request, "translate/catalog.html", {
        "query": query or "",
        "entries": entries_paginated,
        "entries_count": entries.count(),
        "as_translations": as_translations_paginated,
        "page_nums": [str(page_num) for page_num in page_nums],
        "sort_by": sort_by,
    })


def entry(request, entry_pk):
    entry = get_object_or_404(Entry, pk=entry_pk)

    # Get bookmark status
    bookmarked = False
    if entry.bookmarks.filter(pk=request.user.id).exists():
        bookmarked = True

    # Get translations
    translations = sorted(entry.translations.all(), key=lambda t: t.vote_count, reverse=True)

    # Add translation
    if request.method == "POST":
        lang = request.POST.get("lang")
        content = request.POST.get("content")

        if lang != entry.lang.code and content:
            lang_object = get_object_or_404(Language, code=lang)
            translation, created = Translation.objects.get_or_create(
                entry=entry, lang=lang_object, content=content.strip(), user=request.user
            )
            if not created:
                return render(request, "translate/entry.html", {
                    "entry": entry,
                    "bookmarked": bookmarked,
                    "translations": translations,
                    "message": "Translation already exists."
                })

    return render(request, "translate/entry.html", {
        "entry": entry,
        "bookmarked": bookmarked,
        "translations": translations,
    })


@login_required
def add(request):
    if request.method == "POST":
        lang = request.POST.get("lang")
        content = request.POST.get("content")

        if lang and content:
            lang_object = get_object_or_404(Language, code=lang)
            entry, created = Entry.objects.get_or_create(lang=lang_object, content=content.strip(), user=request.user)
            if not created:
                return render(request, "translate/add.html", {"message": "Entry already exists."})
            return redirect("translate:entry", entry.pk)

    return render(request, "translate/add.html")


@login_required
def edit_entry(request, entry_pk):
    entry = get_object_or_404(Entry, pk=entry_pk)

    if request.method == "POST" and entry.user == request.user:
        if content := request.POST.get("content"):
            entry.content = content.strip()
            entry.save()

        return redirect("translate:entry", entry.pk)

    return render(request, "translate/edit_entry.html", {
        "entry": entry,
    })


@login_required
def edit_translation(request, translation_pk):
    translation = get_object_or_404(Translation, pk=translation_pk)

    if request.method == "POST" and translation.user == request.user:
        if content := request.POST.get("content"):
            translation.content = content.strip()
            translation.save()

        return redirect("translate:entry", translation.entry.pk)

    return render(request, "translate/edit_translation.html", {
        "translation": translation,
    })


@login_required
def delete_entry(request):
    if request.method == "POST":
        entry_pk = request.POST.get("entry_pk")

        entry = get_object_or_404(Entry, pk=entry_pk)

        if entry.user == request.user:
            entry.delete()

    if next := request.GET.get("next"):
        return redirect(next)

    return redirect("translate:catalog")


@login_required
def delete_translation(request):
    if request.method == "POST":
        translation_pk = request.POST.get("translation_pk")

        translation = get_object_or_404(Translation, pk=translation_pk)

        if translation.user == request.user:
            translation.delete()

    if next := request.GET.get("next"):
        return redirect(next)

    return redirect("translate:entry", translation.entry.pk)


@login_required
def bookmark(request, entry_pk):
    entry = get_object_or_404(Entry, pk=entry_pk)

    if request.method == "POST" and request.user != entry.user:
        if entry.bookmarks.filter(pk=request.user.id).exists():
            entry.bookmarks.remove(request.user)
        else:
            entry.bookmarks.add(request.user)

    return redirect("translate:entry", entry_pk)


@login_required
def vote(request, translation_pk):
    translation = get_object_or_404(Translation, pk=translation_pk)

    if request.method == "POST" and request.user != translation.user:
        vote = Vote.objects.get_or_create(translation=translation, user=request.user)[0]
        direction = request.POST.get("direction")
        if direction in ("1", "-1") :
            direction = int(direction)
            if vote.direction != direction:
                vote.direction = direction
                vote.save()
            else:
                vote.delete()
        else:
            vote.delete()

    return redirect("translate:entry", translation.entry.pk)
