from rest_framework import serializers
from .models import CustomUser, Team, Player, Game


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'user_type', 'login_count', 'total_time_spent']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        # Hash the password
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # Password is selected only if the value is updating
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'user', 'team', 'height', 'average_score', 'games_played']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        # Exclude 'user' field from if 'user' is given
        if 'user' in validated_data:
            validated_data.pop('user')

        # handle null assigment for team in given data
        if 'team' in validated_data:
            team = validated_data.pop('team')
            if team is None:
                instance.team = None
            else:
                instance.team = team

        instance.height = validated_data.get('height', instance.height)
        instance.average_score = validated_data.get('average_score', instance.average_score)
        instance.games_played = validated_data.get('games_played', instance.games_played)
        instance.save()
        return instance


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, required=False)
    average_score = serializers.SerializerMethodField()
    top_players = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'coach', 'players', 'average_score', 'top_players']

    def get_average_score(self, obj):
        return obj.average_score()

    def get_top_players(self, obj):
        return obj.top_players()

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