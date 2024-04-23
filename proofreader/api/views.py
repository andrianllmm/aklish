from django.http import JsonResponse
from ..proofreader import proofread_text


def proofread(request):
    if text := request.GET.get("text"):
        if lang := request.GET.get("lang"):
            pass
        else:
            lang = "akl"

        checks = proofread_text(text, lang=lang, max_suggestions=3)

        return JsonResponse({
            "checks": checks,
        })