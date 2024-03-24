from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddEntryForm, AddTranslationForm
from .models import Language, Entry, Translation
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
        "entries": Entry.objects.all().order_by("-created_at")
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
            return render(request, "translations/entry.html", {
                "form": form,
                "entry": entry,
                "translations": entry.translations.all().order_by("-created_at"),
            })
    else:
        form = AddTranslationForm()

    return render(request, "translations/entry.html", {
        "form": form,
        "entry": entry,
        "translations": entry.translations.all().order_by("-created_at"),
    })


def search(request):
    return render(request, "translations/search.html")


@login_required(login_url="user:login")
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
            return render(request, "translations/add.html", {
                "form": form
            })
    else:
        form = AddEntryForm()

    return render(request, "translations/add.html", {
        "form": form
    })