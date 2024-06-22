from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Team, Player, Game
from .serializers import CustomUserSerializer, TeamSerializer, PlayerSerializer, GameSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'coach':
            return Team.objects.filter(coach=user)
        return super().get_queryset()

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'coach':
            return Player.objects.filter(team__coach=user)
        return super().get_queryset()

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        games = Game.objects.all()
        serializer = self.get_serializer(games, many=True)
        return Response(serializer.data)
