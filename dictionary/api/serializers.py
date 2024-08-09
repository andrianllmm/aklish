from rest_framework import serializers
from ..models import PartsOfSpeech, Origin, Classification, Attribute, DictEntry
from translate.models import Language, Entry, Translation


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["code"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data["code"]


class PartsOfSpeechSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartsOfSpeech
        fields = ["code"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data["code"]


class OriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Origin
        fields = ["code"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data["code"]


class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = ["code"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data["code"]


class SimilarOppositeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DictEntry
        fields = ["word"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data["word"]


class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ["content"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data["content"]


class AttributeSerializer(serializers.ModelSerializer):
    pos = PartsOfSpeechSerializer()
    origin = OriginSerializer()
    classification = ClassificationSerializer()
    similar = SimilarOppositeSerializer(many=True)
    opposite = SimilarOppositeSerializer(many=True)
    examples = ExampleSerializer(many=True)

    class Meta:
        model = Attribute
        fields = [
            "definition",
            "pos",
            "origin",
            "classification",
            "similar",
            "opposite",
            "examples",
            "sources",
        ]


class DictEntrySerializer(serializers.ModelSerializer):
    lang = LanguageSerializer()
    attributes = AttributeSerializer(many=True)

    class Meta:
        model = DictEntry
        fields = ["word", "lang", "attributes"]
