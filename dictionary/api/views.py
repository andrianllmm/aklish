from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import DictEntry
from translations.models import Language
from .serializers import DictEntrySerializer


@api_view(["GET"])
def define_word(request, lang, word):
    lang_object = Language.objects.get(code=lang)
    dict_entries = DictEntry.objects.get(word=word, lang=lang_object)
    serializer = DictEntrySerializer(dict_entries)
    return Response(serializer.data)