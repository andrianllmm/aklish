from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request, lang):
    return render(request, "proofreader/index.html")
