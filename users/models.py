from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    reputation = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}"

    def update_reputation(self):
        user = self.user

        reputation = 0

        for entry in user.entries.all():
            reputation += 1

            reputation += entry.bookmarks.all().count() * 2
            
        for translation in user.translations.all():
            reputation += 1

            upvote_points = translation.upvote_count() * 10
            reputation += upvote_points + upvote_points * (translation.correctness / 100)
            downvote_points = (translation.downvote_count() * 5)
            reputation -= downvote_points - downvote_points * (translation.correctness / 100)

        self.reputation = round(reputation)
        self.save()