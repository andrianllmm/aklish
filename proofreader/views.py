from django.shortcuts import render
from django.http import JsonResponse
from .proofreader import proofread_text


def index(request):
    if request.method == "GET":
        if text := request.GET.get("text"):
            checks = proofread_text(text, max_suggestions=3)

            return JsonResponse({
                "checks": checks,
            })

    return render(request, "proofreader/index.html")
