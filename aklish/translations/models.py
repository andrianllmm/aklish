from django.db import models
from django.contrib.auth.models import User

from proofreader import proofreader


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
    word_count = models.IntegerField(default=0)
    mistake_count = models.IntegerField(default=0)
    correctness = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("content", "lang")

    def update_word_count(self):
        data = proofreader.proofread_text(self.content, lang=self.lang.code)
        self.word_count = proofreader.cal_word_count(data["checks"])

    def update_mistake_count(self):
        data = proofreader.proofread_text(self.content, lang=self.lang.code)
        self.mistake_count = proofreader.cal_mistake_count(data["checks"])

    def update_correctness(self):
        self.correctness = proofreader.cal_correctness(self.word_count, self.mistake_count)

    def save(self, *args, **kwargs):
        self.update_word_count()
        self.update_mistake_count()
        self.update_correctness()
        self.user.profile.update_reputation()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.content} ({self.lang.code}) by {self.user.username}"


class Translation(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="translations")
    content = models.TextField()
    lang = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="translations")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="translations")
    vote_count = models.IntegerField(default=0)
    word_count = models.IntegerField(default=0)
    mistake_count = models.IntegerField(default=0)
    correctness = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("content", "lang", "entry")

    def update_vote_count(self):
        total = 0
        for vote in self.votes.all():
            total += vote.direction
        self.vote_count = total
        self.save()

    def upvote_count(self):
        return self.votes.filter(direction=1).count()

    def downvote_count(self):
        return self.votes.filter(direction=-1).count()

    def update_word_count(self):
        data = proofreader.proofread_text(self.content, lang=self.lang.code)
        self.word_count = proofreader.cal_word_count(data["checks"])

    def update_mistake_count(self):
        data = proofreader.proofread_text(self.content, lang=self.lang.code)
        self.mistake_count = proofreader.cal_mistake_count(data["checks"])

    def update_correctness(self):
        self.correctness = proofreader.cal_correctness(self.word_count, self.mistake_count)

    def save(self, *args, **kwargs):
        self.update_word_count()
        self.update_mistake_count()
        self.update_correctness()
        self.user.profile.update_reputation()
        super().save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        super(Vote, self).save(*args, **kwargs)

        self.translation.update_vote_count()
        self.translation.user.profile.update_reputation()

        if self.direction == 0:
            self.delete()

    def __str__(self):
        return f"{self.direction} ({self.user.username}) ({self.translation.content})"
