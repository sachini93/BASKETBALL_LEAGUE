from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta

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

    def __str__(self):
        return f"{self.team1} vs {self.team2} - {self.team1_score}:{self.team2_score}"

    def winner(self):
        if self.team1_score > self.team2_score:
            return self.team1
        return self.team2
