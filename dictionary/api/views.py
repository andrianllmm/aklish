import random
from django.db.models.functions import Length
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..models import DictEntry, Attribute
from translations.models import Language
from .serializers import DictEntrySerializer


class DefineWordAPIView(APIView):
    def get(self, request, lang, word=None):
        try:
            lang_object = Language.objects.get(code=lang)
        except Language.DoesNotExist:
            return Response({"error": "Language not found"}, status=status.HTTP_404_NOT_FOUND)

        dict_entries = DictEntry.objects.filter(lang=lang_object)

        if word:
            try:
                dict_entry = dict_entries.get(word=word)
                serializer = DictEntrySerializer(dict_entry)
                return Response(serializer.data)
            except DictEntry.DoesNotExist:
                return Response({"error": "Word not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            filtered_entries = self.apply_filters(dict_entries)
            if filtered_entries.exists():
                random_entry = random.choice(filtered_entries)
                serializer = DictEntrySerializer(random_entry)
                return Response(serializer.data)
            else:
                return Response({"error": "No words found matching the criteria"}, status=status.HTTP_404_NOT_FOUND)

    def apply_filters(self, queryset):
        queryset = self.filter_by_word_len(queryset)
        queryset = self.filter_by_definition_len(queryset)
        queryset = self.filter_by_attribute(queryset)
        return queryset

    def filter_by_word_len(self, queryset):
        if word_len := self.request.query_params.get("word_len"):
            if "-" in word_len:
                min_length, max_length = map(int, word_len.split('-'))
                return queryset.annotate(word_length=Length("word")).filter(word_length__range=(min_length, max_length))
            else:
                return queryset.annotate(word_length=Length("word")).filter(word_length=int(word_len))
        return queryset
    
    def filter_by_definition_len(self, queryset):
        if definition_len := self.request.query_params.get("definition_len"):
            if "-" in definition_len:
                min_length, max_length = map(int, definition_len.split('-'))
                return queryset.annotate(definition_length=Length("attributes__definition")).filter(definition_length__range=(min_length, max_length))
            else:
                return queryset.annotate(definition_length=Length("attributes__definition")).filter(definition_length=int(definition_len))
        return queryset
    
    def filter_by_attribute(self, queryset):
        if poss := self.request.query_params.getlist("pos"):
            queryset = queryset.filter(attributes__pos__code__in=poss)
        if exclude_poss := self.request.query_params.getlist("pos!"):
            queryset = queryset.exclude(attributes__pos__code__in=exclude_poss)

        if classifications := self.request.query_params.getlist("classification"):
            queryset = queryset.filter(attributes__classification__code__in=classifications)
        if exclude_classifications := self.request.query_params.getlist("classification!"):
            queryset = queryset.exclude(attributes__classification__code__in=exclude_classifications)

        return queryset