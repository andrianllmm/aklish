from django.db import models
from django.contrib.auth.models import User
from dictionary.models import DictEntry, Language


class GameStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="game_stats")
    game = models.CharField(max_length=32)
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    winning_rate = models.IntegerField(default=0)
    win_streak = models.IntegerField(default=0)
    max_win_streak = models.IntegerField(default=0)
    solutions = models.ManyToManyField(DictEntry, related_name="game_stats")

    def update_stats(self, won, solution, lang):
        lang_object = Language.objects.get(code=lang)
        solution_entry = DictEntry.objects.get(word=solution, lang=lang_object)
        self.solutions.add(solution_entry)
        self.games_played += 1

        if won:
            self.games_won += 1
            self.win_streak += 1
            if self.win_streak > self.max_win_streak:
                self.max_win_streak = self.win_streak
        else:
            self.win_streak = 0

        if self.games_played > 0:
            self.winning_rate = round((self.games_won / self.games_played) * 100)
        else:
            self.winning_rate = 0

        self.save()
    
    def __str__(self):
        return f"{self.user.username}"