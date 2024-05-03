from django.shortcuts import render
from django.http import JsonResponse
from .proofreader import proofread_text


def index(request, lang):
    return render(request, "proofreader/index.html")
