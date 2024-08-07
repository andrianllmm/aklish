import random
import Levenshtein
from django.db.models import Q
from django.db.models.functions import Length
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from ..models import DictEntry
from translations.models import Language
from .serializers import DictEntrySerializer


class DictEntryFilter:
    @staticmethod
    def word(queryset, request):
        if words := request.query_params.getlist("word"):
            queryset = queryset.filter(word__in=words)
        if exclude_words := request.query_params.getlist("word!"):
            queryset = queryset.exclude(word__in=exclude_words)

        if word_start := request.query_params.get("word^"):
            queryset = queryset.filter(word__startswith=word_start)
        if word_not_start := request.query_params.get("word!^"):
            queryset = queryset.exclude(word__startswith=word_not_start)

        if word_end := request.query_params.get("word$"):
            queryset = queryset.filter(word__endswith=word_end)
        if word_not_end := request.query_params.get("word!$"):
            queryset = queryset.exclude(word__endswith=word_not_end)

        if word_contains := request.query_params.get("word*"):
            queryset = queryset.filter(word__icontains=word_contains)
        if word_not_contains := request.query_params.get("word!*"):
            queryset = queryset.exclude(word__icontains=word_not_contains)

        if word := request.query_params.get("word_advanced"):
            if "_" in word:
                pattern = "^" + word.replace("_", ".") + "$"
                queryset = queryset.filter(word__regex=pattern)

        casing_condition = request.query_params.get("word_case")
        if casing_condition:
            if casing_condition == "lower":
                queryset = queryset.filter(word__regex=r"^[a-z]+$")
            elif casing_condition == "capitalized":
                queryset = queryset.filter(word__regex=r"^[A-Z][a-z]*$")
            elif casing_condition == "upper":
                queryset = queryset.filter(word__regex=r"^[A-Z]+$")

        if word_len := request.query_params.get("word_len"):
            if "-" in word_len:
                min_length, max_length = map(int, word_len.split("-"))
                queryset = queryset.annotate(word_length=Length("word")).filter(
                    word_length__range=(min_length, max_length)
                )
            else:
                queryset = queryset.annotate(word_length=Length("word")).filter(
                    word_length=int(word_len)
                )

        if levenshtein := request.query_params.get("levenshtein"):
            target_word = levenshtein.strip()
            max_distance = 1
            if max_distance_param := request.query_params.get("max_distance"):
                max_distance = max(int(max_distance_param), 5)
            queryset = queryset.filter(
                Q(
                    word__in=[
                        entry.word
                        for entry in DictEntry.objects.all()
                        if 0
                        < Levenshtein.distance(entry.word, target_word)
                        <= max_distance
                    ]
                )
            )

        return queryset

    @staticmethod
    def definition(queryset, request):
        if definition_start := request.query_params.get("definition^"):
            queryset = queryset.filter(
                attributes__definition__startswith=definition_start
            )
        if definition_not_start := request.query_params.get("definition!^"):
            queryset = queryset.exclude(
                attributes__definition__startswith=definition_not_start
            )

        if definition_end := request.query_params.get("definition$"):
            queryset = queryset.filter(attributes__definition__endswith=definition_end)
        if definition_not_end := request.query_params.get("definition!$"):
            queryset = queryset.exclude(
                attributes__definition__endswith=definition_not_end
            )

        if definition_contains := request.query_params.get("definition*"):
            queryset = queryset.filter(
                attributes__definition__icontains=definition_contains
            )
        if definition_not_contains := request.query_params.get("definition!*"):
            queryset = queryset.exclude(
                attributes__definition__icontains=definition_not_contains
            )

        if definition_len := request.query_params.get("definition_len"):
            if "-" in definition_len:
                min_length, max_length = map(int, definition_len.split("-"))
                queryset = queryset.annotate(
                    definition_length=Length("attributes__definition")
                ).filter(definition_length__range=(min_length, max_length))
            else:
                queryset = queryset.annotate(
                    definition_length=Length("attributes__definition")
                ).filter(definition_length=int(definition_len))

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
            queryset = queryset.filter(
                attributes__classification__code__in=classifications
            )
        if exclude_classifications := request.query_params.getlist("classification!"):
            queryset = queryset.exclude(
                attributes__classification__code__in=exclude_classifications
            )

        return queryset

    @staticmethod
    def has(queryset, request):
        if has := request.query_params.getlist("has"):
            if "similar" in has:
                queryset = queryset.filter(attributes__similar__isnull=False)
            if "opposite" in has:
                queryset = queryset.filter(attributes__opposite__isnull=False)

        if has_no := request.query_params.getlist("has!"):
            if "similar" in has_no:
                queryset = queryset.filter(attributes__similar__isnull=True)
            if "opposite" in has_no:
                queryset = queryset.filter(attributes__opposite__isnull=True)

        return queryset


class ListDictEntryAPIView(APIView):
    @method_decorator(ratelimit(key="user_or_ip", rate="60/m"))
    def get(self, request, lang):
        try:
            lang_object = Language.objects.get(code=lang)
        except Language.DoesNotExist:
            return Response(
                {"error": "Language not found"}, status=status.HTTP_404_NOT_FOUND
            )

        dict_entries = DictEntry.objects.filter(lang=lang_object)

        filtered_entries = DictEntryFilter.word(dict_entries, request)
        filtered_entries = DictEntryFilter.definition(filtered_entries, request)
        filtered_entries = DictEntryFilter.attribute(filtered_entries, request)

        if filtered_entries.exists():
            num_entries = self.get_num_entries(request)
            sliced_entries = filtered_entries.order_by("?")[:num_entries]
            serializer = DictEntrySerializer(sliced_entries, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "No words found matching the criteria"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def get_num_entries(self, request):
        default_num_entries = 5
        num_entries = request.query_params.get("num", default_num_entries)
        try:
            num_entries = int(num_entries)
            num_entries = max(min(num_entries, 10), 1)
        except ValueError:
            num_entries = default_num_entries
        return num_entries


class RetrieveDictEntryAPIView(APIView):
    @method_decorator(ratelimit(key="user_or_ip", rate="60/m"))
    def get(self, request, lang, word=None):
        try:
            lang_object = Language.objects.get(code=lang)
        except Language.DoesNotExist:
            return Response(
                {"error": "Language not found"}, status=status.HTTP_404_NOT_FOUND
            )

        dict_entries = DictEntry.objects.filter(lang=lang_object)

        if word:
            try:
                dict_entry = dict_entries.get(word=word)
                serializer = DictEntrySerializer(dict_entry)
                return Response(serializer.data)
            except DictEntry.DoesNotExist:
                return Response(
                    {"error": "Word not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            filtered_entries = DictEntryFilter.word(dict_entries, request)
            filtered_entries = DictEntryFilter.definition(filtered_entries, request)
            filtered_entries = DictEntryFilter.attribute(filtered_entries, request)
            filtered_entries = DictEntryFilter.has(filtered_entries, request)

            if filtered_entries.exists():
                random_entry = random.choice(filtered_entries)
                serializer = DictEntrySerializer(random_entry)
                return Response(serializer.data)
            else:
                return Response(
                    {"error": "No words found matching the criteria"},
                    status=status.HTTP_404_NOT_FOUND,
                )
