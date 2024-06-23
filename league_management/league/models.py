from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta
import numpy as np

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('coach', 'Coach'),
        ('player', 'Player'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    login_count = models.IntegerField(default=0)
    total_time_spent = models.DurationField(default=timedelta())

class Team(models.Model):
    name = models.CharField(max_length=100)
    coach = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='team')

    def average_score(self):
        # Related name for players in the team
        players = self.players.all()
        if players:
            total_score = sum(player.average_score for player in players)
            return total_score / players.count()
        return 0

    def top_players(self):
        players = self.players.all()

        # check if there are players in the team
        if not players.exists():
            return []

        # Calculate the 90th percentile score
        scores = np.array([player.average_score for player in players])
        percentile_90 = np.percentile(scores, 90)
        top_players = players.filter(average_score__gte=percentile_90)

        return [player.user.id for player in top_players]

    def __str__(self):
        return self.name

class Player(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    height = models.FloatField()
    average_score = models.FloatField(default=0)
    games_played = models.IntegerField(default=0)

    def __str__(self):
        return self.user.name

class Game(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_games')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_games')
    team1_score = models.IntegerField()
    team2_score = models.IntegerField()
    date = models.DateField()

    def get_winner(self):
        if self.team1_score > self.team2_score:
            return self.team1.name
        return self.team2.name

    def __str__(self):
        return f"{self.team1} vs {self.team2} - {self.team1_score}:{self.team2_score}"
