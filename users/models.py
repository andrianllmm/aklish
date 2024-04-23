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
        for translation in user.translations.all():
            reputation += translation.upvote_count() * 10
            reputation -= translation.downvote_count() * 5

        self.reputation = reputation
        self.save()