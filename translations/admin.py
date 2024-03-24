from django.contrib import admin
from .models import Language, Entry, Translation



admin.site.register(Language)
admin.site.register(Entry)
admin.site.register(Translation)