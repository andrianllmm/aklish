from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Entry(models.Model):
    content = models.TextField()
    lang = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="texts")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="texts")

    class Meta:
        unique_together = ("content", "lang")
    
    def __str__(self):
        return f"{self.content} ({self.lang.code}) by {self.user.username}"


class Translation(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="translations")
    content = models.TextField()
    lang = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="translations")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="translations")

    class Meta:
        unique_together = ("content", "lang", "entry")

    def __str__(self):
        return f"{self.entry} to {self.content} ({self.lang.code}) by {self.user.username}"