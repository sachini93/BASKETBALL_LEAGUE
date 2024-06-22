from rest_framework import serializers
from .models import CustomUser, Team, Player, Game

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type', 'login_count', 'total_time_spent']

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['user', 'height', 'average_score', 'games_played']

class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'coach', 'players']

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['team1', 'team2', 'team1_score', 'team2_score', 'date']
