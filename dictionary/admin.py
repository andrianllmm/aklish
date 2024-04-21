from django.contrib import admin
from .models import PartsOfSpeech, Origin, Classification, Attribute, DictEntry


admin.site.register(PartsOfSpeech)
admin.site.register(Origin)
admin.site.register(Classification)
admin.site.register(Attribute)
admin.site.register(DictEntry)