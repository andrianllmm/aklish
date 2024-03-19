from django.db import models

# Create your models here.
class DictEntry(models.Model):
    word = models.CharField(max_length=100)
    definition = models.TextField()

    def __str__(self):
        return f"{self.word}"