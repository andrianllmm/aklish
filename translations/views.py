from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AddEntryForm, AddTranslationForm
from .models import Language, Entry, Translation, Vote
from dictionary.models import DictEntry


def homepage(request):
    return render(request, "translations/homepage.html", {
        "entries": Entry.objects.all(),
        "translations": Translation.objects.all(),
        "dict_entries": DictEntry.objects.all()
    })


def catalog(request):
    if query := request.GET.get("q"):
        return render(request, "translations/catalog.html", {
            "entries": Entry.objects.filter(content__icontains=query)
        })
    
    return render(request, "translations/catalog.html", {
        "entries": Entry.objects.all().order_by("?")
    })


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
    
    translations = sorted(entry.translations.all(), key=lambda t: t.vote_count(), reverse=True)
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


def search(request):
    return render(request, "translations/search.html")


@login_required(login_url="users:login")
def add(request):
    if request.method == "POST":
        form = AddEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()

            translation_content = form.cleaned_data["translation_content"]
            translation_lang = form.cleaned_data["translation_lang"]
            if translation_content and translation_lang:
                translation, created= Translation.objects.get_or_create(
                    entry=entry, content=translation_content, lang=translation_lang, user=request.user
                )
                if request.POST.get("reverse"):
                    entry_reverse, created = Entry.objects.get_or_create(
                        content=translation_content, lang=translation_lang, user=request.user
                    )
                    translation_reverse, created = Translation.objects.get_or_create(
                        entry=entry_reverse, content=entry.content, lang=entry.lang, user=request.user
                    )
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