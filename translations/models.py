from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class TextEntry(models.Model):
    content = models.TextField()
    lang = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="texts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="text_entries")

    def __str__(self):
        return f"{self.content} ({self.lang.code}) by {self.user.username}"
    
    class Meta:
        unique_together = ("content", "lang")


class TranslationEntry(models.Model):
    source = models.OneToOneField(TextEntry, on_delete=models.CASCADE, related_name="requests")
    target = models.ManyToManyField(TextEntry, blank=True, related_name="responses")

    def __str__(self):
        if len(self.target.all()) > 0:
            return f"{self.source.content} ({self.source.lang.name} => {self.target.all()[0].lang.name})"
        else:
            return f"{self.source.content} ({self.source.lang.name} => NA)"