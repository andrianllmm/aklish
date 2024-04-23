from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import AddEntryForm, AddTranslationForm
from .models import Language, Entry, Translation, Vote
from dictionary.models import DictEntry


def homepage(request):
    return render(request, "translations/homepage.html", {
        "entries": Entry.objects.all(),
        "translations": Translation.objects.all(),
        "dict_entries": DictEntry.objects.all(),
    })


def catalog(request):
    entries = Entry.objects.all().order_by("created_at")

    p = Paginator(entries, 15)
    page = request.GET.get("page") if request.GET.get("page") else 1
    entries = p.get_page(page)

    start = max(1, entries.number - 3)
    end = min(start + 6, entries.paginator.num_pages)
    page_nums = (range(start, end + 1))

    return render(request, "translations/catalog.html", {
        "entries": entries,
        "page_nums": [str(page_num) for page_num in page_nums],
    })


def search(request):
    if query := request.GET.get("q"):
        entries = Entry.objects.filter(content__icontains=query).order_by("content")
        as_translations = Entry.objects.filter(translations__content__icontains=query).order_by("content")

        entries_paginator = Paginator(entries, 30)
        as_translations_paginator = Paginator(as_translations, 30)
        page = request.GET.get("page") if request.GET.get("page") else 1
        entries = entries_paginator.get_page(page)
        if int(page) > entries.paginator.num_pages:
            entries = None
        as_translations = as_translations_paginator.get_page(page)
        if int(page) > as_translations.paginator.num_pages:
            as_translations = None

        start = max(1, entries.number - 3)
        end = min(start + 6, entries.paginator.num_pages)
        page_nums = (range(start, end + 1))

        return render(request, "translations/search.html", {
            "query": query,
            "entries": entries,
            "as_translations": as_translations,
            "page_nums": [str(page_num) for page_num in page_nums]
        })
    else:
        return render(request, "translations/search.html")


def entry(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)

    if request.method == "POST":
        form = AddTranslationForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            lang = form.cleaned_data["lang"]
            if content and lang:
                translation, created = Translation.objects.get_or_create(
                    entry=entry, content=content, lang=lang, user=request.user
                )
                if request.POST.get("reverse"):
                    entry_reverse, created = Entry.objects.get_or_create(
                        content=content, lang=lang, user=request.user
                    )
                    translation_reverse, created = Translation.objects.get_or_create(
                        entry=entry_reverse, content=entry.content, lang=entry.lang, user=request.user
                    )
    else:
        form = AddTranslationForm()
    
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
        "form": form,
        "entry": entry,
        "bookmarked": bookmarked,
        "translations_votes": translations_votes,
    })


@login_required(login_url="users:login")
def add(request):
    if request.method == "POST":
        form = AddEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect("translations:entry", entry.pk)
    else:
        form = AddEntryForm()

    return render(request, "translations/add.html", {
        "form": form
    })


def bookmark(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    if request.method == "POST":
        if request.user.is_authenticated:
            if entry.bookmarks.filter(pk=request.user.id).exists():
                entry.bookmarks.remove(request.user)
            else:
                entry.bookmarks.add(request.user)
        else:
            return redirect("users:login")
    return redirect("translations:entry", entry_id)


def vote(request, translation_id):
    translation = get_object_or_404(Translation, pk=translation_id)
    if request.method == "POST":
        if request.user.is_authenticated:
            vote, created = Vote.objects.get_or_create(translation=translation, user=request.user)
            if request.POST.get("upvote"):
                vote.direction = 1 if vote.direction != 1 else 0
            elif request.POST.get("downvote"):
                vote.direction = -1 if vote.direction != -1 else 0
            vote.save()
        else:
            return redirect("users:login")
    return redirect("translations:entry", translation.entry.pk)