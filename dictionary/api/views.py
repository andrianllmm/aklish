import random
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import DictEntry
from translations.models import Language
from .serializers import DictEntrySerializer


@api_view(["GET"])
def define_word(request, lang, word=None):
    lang_object = Language.objects.get(code=lang)
    dict_entries = DictEntry.objects.filter(lang=lang_object)
    if word:
        dict_entry = dict_entries.get(word=word)
    else:
        pks = dict_entries.values_list('pk', flat=True)
        random_pk = random.choice(pks)
        dict_entry = dict_entries.get(pk=random_pk)
    serializer = DictEntrySerializer(dict_entry)
    return Response(serializer.data)