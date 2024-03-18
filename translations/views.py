from django.shortcuts import render, redirect
from .models import Language, TextEntry, TranslationEntry

# Create your views here.
def homepage(request):
    return render(request, "translations/homepage.html")


def translations(request):
    if query := request.GET.get("q"):
        return render(request, "translations/translations.html", {
        "translations": TranslationEntry.objects.filter(source__content__contains=query)
        })
    return render(request, "translations/translations.html", {
        "translations": TranslationEntry.objects.all()
    })


def translation_entry(request, translation_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            add(request)
        else:
            return redirect("user:login")

    translation_entry = TranslationEntry.objects.get(pk=translation_id)
    return render(request, "translations/translation_entry.html", {
        "translation_entry": translation_entry,
        "targets": translation_entry.target.all()
    })


def texts(request):
    return render(request, "translations/texts.html", {
        "texts": TextEntry.objects.all()
    })


def search(request):
    return render(request, "translations/search.html")


def add(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            source_lang = Language.objects.get(code=request.POST.get("source_lang"))
            source_content = request.POST.get("source_content")
            target_lang = Language.objects.get(code=request.POST.get("target_lang"))
            target_content = request.POST.get("target_content")

            if source_lang == target_lang:
                return redirect(request.path_info)

            if TextEntry.objects.filter(content=source_content, lang=source_lang).exists():
                source = TextEntry.objects.get(content=source_content, lang=source_lang)
            else:
                source = TextEntry(content=source_content, lang=source_lang, user=user)
                if len(source.content) > 0:
                    source.save()
                else:
                    return redirect(request.path_info)
        
            if TextEntry.objects.filter(content=target_content, lang=target_lang).exists():
                target = TextEntry.objects.get(content=target_content, lang=target_lang)
            else:
                target = TextEntry(content=target_content, lang=target_lang, user=user)
                if len(target.content) > 0:
                    target.save()
                else:
                    target = 0
        
            if TranslationEntry.objects.filter(source=source).exists():
                t = TranslationEntry.objects.get(source=source)
            else:
                t = TranslationEntry(source=source)
                t.save()

            if target:
                t.target.add(target)

            return redirect(request.path_info)
        else:
            return redirect("user:login")
    return render(request, "translations/add.html")