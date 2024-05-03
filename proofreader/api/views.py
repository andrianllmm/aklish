from django.http import JsonResponse
from ..proofreader import proofread_text


def proofread(request, lang="akl"):
    if text := request.GET.get("text"):
        checks = proofread_text(text, lang=lang, max_suggestions=3)

        return JsonResponse({
            "checks": checks,
        })