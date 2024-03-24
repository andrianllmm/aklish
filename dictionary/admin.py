from django.contrib import admin
from .models import PartsOfSpeech, Etymology, Classification, Attribute, DictEntry


admin.site.register(PartsOfSpeech)
admin.site.register(Etymology)
admin.site.register(Classification)
admin.site.register(Attribute)
admin.site.register(DictEntry)