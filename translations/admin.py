from django.contrib import admin
from .models import Language, TextEntry, TranslationEntry

# Register your models here.
admin.site.register(Language)
admin.site.register(TextEntry)
admin.site.register(TranslationEntry)