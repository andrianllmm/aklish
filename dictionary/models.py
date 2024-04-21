from django.db import models
from translations.models import Language, Entry


class PartsOfSpeech(models.Model):
    code = models.CharField(max_length=5, unique=True)
    meaning = models.CharField(max_length=64)

    class Meta:
        unique_together = ("code", "meaning")

    def __str__(self):
        return f"{self.meaning} ({self.code})"


class Origin(models.Model):
    code = models.CharField(max_length=3, unique=True)
    meaning = models.CharField(max_length=64)

    class Meta:
        unique_together = ("code", "meaning")

    def __str__(self):
        return f"{self.meaning} ({self.code})"


class Classification(models.Model):
    code = models.CharField(max_length=4, unique=True)
    meaning = models.CharField(max_length=64)

    class Meta:
        unique_together = ("code", "meaning")

    def __str__(self):
        return f"{self.meaning} ({self.code})"


class Attribute(models.Model):
    definition = models.TextField()
    pos = models.ForeignKey(PartsOfSpeech, on_delete=models.PROTECT, null=True, blank=True, related_name="attributes")
    origin = models.ForeignKey(Origin, on_delete=models.PROTECT, null=True, blank=True, related_name="attributes")
    classification = models.ForeignKey(Classification, on_delete=models.PROTECT, null=True, blank=True, related_name="attributes")
    similar = models.ManyToManyField("DictEntry", blank=True, related_name="similar")
    opposite = models.ManyToManyField("DictEntry", blank=True, related_name="opposite")
    examples = models.ManyToManyField(Entry, blank=True, related_name="example_of")
    source = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.definition} ({self.pos.code})"


class DictEntry(models.Model):
    word = models.CharField(max_length=100)
    lang = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="dict_entries")
    attributes = models.ManyToManyField(Attribute, blank=True, related_name="entry")

    class Meta:
        unique_together = ("word", "lang")

    def __str__(self):
        return f"{self.word} ({self.lang.code})"