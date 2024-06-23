from rest_framework import serializers
from .models import CustomUser, Team, Player, Game


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type', 'login_count', 'total_time_spent']


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'user', 'team', 'height', 'average_score', 'games_played']
        read_only_fields = ['id']


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, required=False)
    average_score = serializers.SerializerMethodField()
    # top_players = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'coach', 'players', 'average_score']

    def get_average_score(self, obj):
        return obj.average_score()

    # def get_top_players(self, obj):
    #     print('serializer:', obj.top_players())
    #     return PlayerSerializer(obj.top_players()).data

    def update(self, instance, validated_data):
        players_data = validated_data.pop('players', [])
        instance.name = validated_data.get('name', instance.name)
        instance.coach = validated_data.get('coach', instance.coach)
        instance.save()

        # Handle updating players
        for player_data in players_data:
            player_id = player_data.get('id')
            if player_id:
                player = Player.objects.get(id=player_id, team=instance)
                player.height = player_data.get('height', player.height)
                player.average_score = player_data.get('average_score', player.average_score)
                player.games_played = player_data.get('games_played', player.games_played)
                player.save()
            else:
                Player.objects.create(team=instance, **player_data)

        return instance

    def create(self, validated_data):
        players_data = validated_data.pop('players', [])
        team = Team.objects.create(**validated_data)
        for player_data in players_data:
            Player.objects.create(team=team, **player_data)
        return team


class GameSerializer(serializers.ModelSerializer):
    winner = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ['id', 'team1', 'team2', 'team1_score', 'team2_score', 'date', 'winner']

    def get_winner(self, obj):
        winner_team = obj.get_winner()
        return winner_team