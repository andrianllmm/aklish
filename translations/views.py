from django.shortcuts import render, redirect
from .models import Language, Entry, Translation
from dictionary.models import DictEntry

# Create your views here.
def homepage(request):
    text_count = len(Entry.objects.all())
    translation_count = len(Translation.objects.all())
    word_count = len(DictEntry.objects.all())
    return render(request, "translations/homepage.html", {
        "text_count": text_count,
        "translation_count": translation_count,
        "word_count": word_count,
    })


def catalog(request):
    if query := request.GET.get("q"):
        return render(request, "translations/catalog.html", {
        "entries": Entry.objects.filter(content__contains=query)
        })
    
    return render(request, "translations/catalog.html", {
        "entries": Entry.objects.all()
    })


def entry(request, entry_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            add(request)
        else:
            return redirect("user:login")

    entry = Entry.objects.get(pk=entry_id)
    return render(request, "translations/entry.html", {
        "entry": entry,
        "translations": entry.translations.all(),
    })


def search(request):
    return render(request, "translations/search.html")


def add(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            lang = Language.objects.get(code=request.POST.get("lang"))
            content = request.POST.get("content")
            translation_lang = Language.objects.get(code=request.POST.get("translation_lang"))
            translation_content = request.POST.get("translation_content")

            if lang == translation_lang:
                return redirect(request.path_info)

            if Entry.objects.filter(content=content, lang=lang).exists():
                entry = Entry.objects.get(content=content, lang=lang)
            else:
                entry = Entry(content=content, lang=lang, user=user)
                if len(content) > 0:
                    entry.save()
                else:
                    return redirect(request.path_info)
            
            translation = Translation(
                entry=entry, content=translation_content, lang=translation_lang, user=user
            )
            if len(translation.content) > 0:
                translation.save()
                entry.translations.add(translation)
    
            return redirect(request.path_info)
        else:
            return redirect("user:login")
    return render(request, "translations/add.html")