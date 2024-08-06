from django.contrib import admin
from .models import PartsOfSpeech, Origin, Classification, Source, Attribute, DictEntry


admin.site.register(PartsOfSpeech)
admin.site.register(Origin)
admin.site.register(Classification)
admin.site.register(Source)
admin.site.register(Attribute)
admin.site.register(DictEntry)