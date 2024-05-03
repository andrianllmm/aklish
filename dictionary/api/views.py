import random
from django.db.models.functions import Length
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..models import DictEntry
from translations.models import Language
from .serializers import DictEntrySerializer


class DictEntryFilter:
    @staticmethod
    def word_len(queryset, request):
        if word_len := request.query_params.get("word_len"):
            if "-" in word_len:
                min_length, max_length = map(int, word_len.split('-'))
                queryset = queryset.annotate(word_length=Length("word")).filter(word_length__range=(min_length, max_length))
            else:
                queryset = queryset.annotate(word_length=Length("word")).filter(word_length=int(word_len))
        return queryset

    @staticmethod
    def definition_len(queryset, request):
        if definition_len := request.query_params.get("definition_len"):
            if "-" in definition_len:
                min_length, max_length = map(int, definition_len.split('-'))
                queryset = queryset.annotate(definition_length=Length("attributes__definition")).filter(definition_length__range=(min_length, max_length))
            else:
                queryset = queryset.annotate(definition_length=Length("attributes__definition")).filter(definition_length=int(definition_len))
        return queryset
    
    @staticmethod
    def attribute(queryset, request):
        if poss := request.query_params.getlist("pos"):
            queryset = queryset.filter(attributes__pos__code__in=poss)
        if exclude_poss := request.query_params.getlist("pos!"):
            queryset = queryset.exclude(attributes__pos__code__in=exclude_poss)
        
        if origins := request.query_params.getlist("origin"):
            queryset = queryset.filter(attributes__origin__code__in=origins)
        if exclude_origins := request.query_params.getlist("origin!"):
            queryset = queryset.exclude(attributes__origin__code__in=exclude_origins)

        if classifications := request.query_params.getlist("classification"):
            queryset = queryset.filter(attributes__classification__code__in=classifications)
        if exclude_classifications := request.query_params.getlist("classification!"):
            queryset = queryset.exclude(attributes__classification__code__in=exclude_classifications)

        return queryset
    
    @staticmethod
    def has(queryset, request):
        if has := request.query_params.getlist("has"):
            if "similar" in has:
                queryset = queryset.filter(attributes__similar__isnull=False)
            if "oppposite" in has:
                queryset = queryset.filter(attributes__opposite__isnull=False)

        if has_no := request.query_params.getlist("has!"):
            if "similar" in has_no:
                queryset = queryset.filter(attributes__similar__isnull=True)
            if "oppposite" in has_no:
                queryset = queryset.filter(attributes__opposite__isnull=True)

        return queryset


class ListDictEntryAPIView(APIView):
    def get(self, request, lang):
        try:
            lang_object = Language.objects.get(code=lang)
        except Language.DoesNotExist:
            return Response({"error": "Language not found"}, status=status.HTTP_404_NOT_FOUND)

        dict_entries = DictEntry.objects.filter(lang=lang_object)

        filtered_entries = DictEntryFilter.word_len(dict_entries, request)
        filtered_entries = DictEntryFilter.definition_len(filtered_entries, request)
        filtered_entries = DictEntryFilter.attribute(filtered_entries, request)
        
        if filtered_entries.exists():
            num_entries = self.get_num_entries(request)
            sliced_entries = filtered_entries.order_by("?")[:num_entries]
            serializer = DictEntrySerializer(sliced_entries, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "No words found matching the criteria"}, status=status.HTTP_404_NOT_FOUND)
    
    def get_num_entries(self, request):
        default_num_entries = 5
        num_entries = request.query_params.get("num", default_num_entries)
        try:
            num_entries = int(num_entries)
            num_entries = max(min(num_entries, 10), 2)
        except ValueError:
            num_entries = default_num_entries
        return num_entries

class RetrieveDictEntryAPIView(APIView):
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
            filtered_entries = DictEntryFilter.word_len(dict_entries, request)
            filtered_entries = DictEntryFilter.definition_len(filtered_entries, request)
            filtered_entries = DictEntryFilter.attribute(filtered_entries, request)
            filtered_entries = DictEntryFilter.has(filtered_entries, request)
            
            if filtered_entries.exists():
                random_entry = random.choice(filtered_entries)
                serializer = DictEntrySerializer(random_entry)
                return Response(serializer.data)
            else:
                return Response({"error": "No words found matching the criteria"}, status=status.HTTP_404_NOT_FOUND)
