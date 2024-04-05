from django.shortcuts import render
from django.http import JsonResponse
from .spellchecker import spellcheck_text


def index(request):
    if request.method == "GET":
        if text := request.GET.get("text"):
            checks = spellcheck_text(text, max_suggestions=3)

            return JsonResponse({
                "checks": checks,
            })

    return render(request, "spellchecker/index.html")
