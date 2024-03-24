from django.db import models


class PartsOfSpeech(models.Model):
    code = models.CharField(max_length=5, unique=True)
    meaning = models.CharField(max_length=64)

    class Meta:
        unique_together = ("code", "meaning")

    def __str__(self):
        return f"{self.meaning} ({self.code})"


class Etymology(models.Model):
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
    pos = models.ForeignKey(PartsOfSpeech, on_delete=models.PROTECT, null=True, related_name="entries")
    etymology = models.ForeignKey(Etymology, on_delete=models.PROTECT, null=True, related_name="entries")
    classification = models.ForeignKey(Classification, on_delete=models.PROTECT, null=True, related_name="entries")

    def __str__(self):
        return f"{self.definition} ({self.pos}; {self.etymology}; {self.classification})"


class DictEntry(models.Model):
    word = models.CharField(max_length=100, unique=True)
    attributes = models.ManyToManyField(Attribute, blank=True, related_name="entry")

    def __str__(self):
        return f"{self.word}"