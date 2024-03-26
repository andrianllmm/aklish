from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=64)

    class Meta:
        unique_together = ("name", "code")

    def __str__(self):
        return f"{self.name} ({self.code})"


class Entry(models.Model):
    content = models.TextField()
    lang = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="entries")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="entries")
    bookmarks = models.ManyToManyField(User, blank=True, related_name="bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("content", "lang")
    
    def __str__(self):
        return f"{self.content} ({self.lang.code}) by {self.user.username}"


class Translation(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="translations")
    content = models.TextField()
    lang = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="translations")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="translations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("content", "lang", "entry")
    
    def vote_count(self):
        total = 0
        for vote in self.votes.all():
            total += vote.direction
        return total

    def __str__(self):
        return f"{self.entry} to {self.content} ({self.lang.code}) by {self.user.username}"


class Vote(models.Model):
    DIRECTIONS = [
        (1, "upvote"),
        (-1, "downvote"),
    ]

    translation = models.ForeignKey(Translation, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    direction = models.IntegerField(default=0, choices=DIRECTIONS)

    class Meta:
        unique_together = ("translation", "user")

    def __str__(self):
        return f"{self.direction} ({self.user.username}) ({self.translation.content})"
