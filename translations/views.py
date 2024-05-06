from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Language, Entry, Translation, Vote
from dictionary.models import DictEntry


def homepage(request):
    return render(request, "translations/homepage.html", {
        "entries": Entry.objects.all(),
        "translations": Translation.objects.all(),
        "dict_entries": DictEntry.objects.all(),
    })


def catalog(request):
    sort = request.GET.get("sort", "latest")

    match sort:
        case "latest":
            entries = Entry.objects.all().order_by("-modified_at")
        case "top":
            entries = Entry.objects.annotate(num_bookmarks=Count('bookmarks')) \
                .order_by("-num_bookmarks")
        case "reputable":
            entries = Entry.objects.all().order_by("-user__profile__reputation")
        case "proofread":
            entries = Entry.objects.all().order_by("-correctness")
        case "translated":
            entries = Entry.objects.annotate(num_translations=Count("translations")) \
                .filter(translations__isnull=False).distinct() \
                .order_by("-num_translations", "-modified_at")
        case "untranslated":
            entries = Entry.objects.filter(translations__isnull=True).distinct().order_by("-modified_at")

    p = Paginator(entries, 15)
    page = request.GET.get("page") if request.GET.get("page") else 1
    entries_paginated = p.get_page(page)

    start = max(1, entries_paginated.number - 3)
    end = min(start + 6, entries_paginated.paginator.num_pages)
    page_nums = (range(start, end + 1))

    return render(request, "translations/catalog.html", {
        "entries": entries_paginated,
        "entries_count": entries.count(),
        "page_nums": [str(page_num) for page_num in page_nums],
        "sort": sort,
    })


def search(request):
    sort = request.GET.get("sort", "latest")

    match sort:
        case "latest":
            entries = Entry.objects.all().order_by("-modified_at")
        case "top":
            entries = Entry.objects.annotate(num_bookmarks=Count('bookmarks')) \
                .order_by("-num_bookmarks")
        case "reputable":
            entries = Entry.objects.all().order_by("-user__profile__reputation")
        case "proofread":
            entries = Entry.objects.all().order_by("-correctness")
        case "translated":
            entries = Entry.objects.annotate(num_translations=Count("translations")) \
                .filter(translations__isnull=False).distinct() \
                .order_by("-num_translations", "-modified_at")
        case "untranslated":
            entries = Entry.objects.filter(translations__isnull=True).distinct().order_by("-modified_at")

    if query := request.GET.get("q"):
        as_translations = entries.filter(translations__content__icontains=query).order_by("content")
        entries = entries.filter(content__icontains=query).order_by("content")

        entries_paginator = Paginator(entries, 30)
        as_translations_paginator = Paginator(as_translations, 30)
        page = request.GET.get("page") if request.GET.get("page") else 1
        entries_paginated = entries_paginator.get_page(page)
        if int(page) > entries_paginated.paginator.num_pages:
            entries_paginated = None
        as_translations_paginated = as_translations_paginator.get_page(page)
        if int(page) > as_translations_paginated.paginator.num_pages:
            as_translations_paginated = None

        start = max(1, entries_paginated.number - 3)
        end = min(start + 6, entries_paginated.paginator.num_pages)
        page_nums = (range(start, end + 1))

        return render(request, "translations/search.html", {
            "query": query,
            "entries": entries_paginated,
            "entries_count": entries.count(),
            "as_translations": as_translations_paginated,
            "page_nums": [str(page_num) for page_num in page_nums],
            "sort": sort,
        })
    else:
        return render(request, "translations/search.html")


def entry(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)

    if request.method == "POST":
        if lang := request.POST.get("lang"):
            if content := request.POST.get("content"):
                lang_object = Language.objects.get(code=lang)
                if lang_object != entry.lang:
                    Translation.objects.create(entry=entry, lang=lang_object, content=content.strip(), user=request.user)
    
    bookmarked = False
    if entry.bookmarks.filter(pk=request.user.id).exists():
        bookmarked = True
    
    translations = sorted(entry.translations.all(), key=lambda t: t.vote_count, reverse=True)
    translations_votes = []
    for translation in translations:
        if request.user.is_authenticated:
            vote, created = translation.votes.get_or_create(translation=translation, user=request.user)
        else:
            vote = False
        translation_vote = (translation, vote)
        translations_votes.append(translation_vote)

    return render(request, "translations/entry.html", {
        "entry": entry,
        "bookmarked": bookmarked,
        "translations_votes": translations_votes,
    })


@login_required(login_url="users:login")
def add(request):
    if request.method == "POST":
        if lang := request.POST.get("lang"):
            if content := request.POST.get("content"):
                lang_object = Language.objects.get(code=lang)
                entry = Entry.objects.create(lang=lang_object, content=content.strip(), user=request.user)
                return redirect("translations:entry", entry.pk)

    return render(request, "translations/add.html")


@login_required(login_url="users:login")
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)

    if entry.user == request.user:

        if request.method == "POST":
            if content := request.POST.get("content"):
                entry.content = content.strip()
                entry.save()

            return redirect("translations:entry", entry.entry.pk)

    return render(request, "translations/edit_entry.html", {
        "entry": entry,
    })


@login_required(login_url="users:login")
def edit_translation(request, translation_id):
    translation = get_object_or_404(Translation, pk=translation_id)

    if translation.user == request.user:

        if request.method == "POST":
            if content := request.POST.get("content"):
                translation.content = content.strip()
                translation.save()
            
            return redirect("translations:entry", translation.entry.pk)

    return render(request, "translations/edit_translation.html", {
        "translation": translation,
    })


@login_required(login_url="users:login")
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)

    if entry.user == request.user:
        entry.delete()
    
    if next := request.GET.get("next"):
        return redirect(next)

    return render(request, "translations/edit_entry.html", {
        "entry": entry,
    })


@login_required(login_url="users:login")
def delete_translation(request, translation_id):
    translation = get_object_or_404(Translation, pk=translation_id)

    if translation.user == request.user:
        translation.delete()
    
    if next := request.GET.get("next"):
        return redirect(next)

    return render(request, "translations/edit_translation.html", {
        "translation": translation,
    })


@login_required(login_url="users:login")
def bookmark(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)

    if request.method == "POST":
        if request.user != entry.user:
            if entry.bookmarks.filter(pk=request.user.id).exists():
                entry.bookmarks.remove(request.user)
            else:
                entry.bookmarks.add(request.user)

    return redirect("translations:entry", entry_id)


@login_required(login_url="users:login")
def vote(request, translation_id):
    translation = get_object_or_404(Translation, pk=translation_id)

    if request.method == "POST":
        if request.user != translation.user:
            vote, created = Vote.objects.get_or_create(translation=translation, user=request.user)
            if request.POST.get("upvote"):
                vote.direction = 1
                vote.save()
            elif request.POST.get("downvote"):
                vote.direction = -1
                vote.save()
            elif request.POST.get("remove"):
                vote.delete()

    return redirect("translations:entry", translation.entry.pk)