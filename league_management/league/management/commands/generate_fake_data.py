import random
from django.core.management.base import BaseCommand
from faker import Faker
from league.models import CustomUser, Team, Player, Game


class Command(BaseCommand):
    help = 'Generate fake users, teams, players, and games'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # # Create Admin User
        # admin_name_postfix = random.randint(1, 10)
        # admin_user = CustomUser.objects.create_superuser(f'admin_{admin_name_postfix}', f'admin{admin_name_postfix}@example.com', 'password')
        # self.stdout.write(self.style.SUCCESS('Admin user created'))

        # Create Coaches
        coaches = []
        for _ in range(10):
            username = fake.user_name()
            user = CustomUser.objects.create_user(username, f'{username}@example.com', 'password')
            coaches.append(user)
            self.stdout.write(self.style.SUCCESS(f'Coach {username} created'))

        # Create Teams
        teams = []
        for i in range(10):
            team_name = f'Team {chr(65 + i)}'
            team = Team.objects.create(name=team_name, coach=coaches[i])
            teams.append(team)
            self.stdout.write(self.style.SUCCESS(f'Team {team_name} created'))

        # Create Players
        for team in teams:
            for _ in range(3):
                username = fake.user_name()
                user = CustomUser.objects.create_user(username, f'{username}@example.com', 'password')
                Player.objects.create(user=user, team=team, height=random.randrange(150, 200), average_score=random.uniform(0, 100), games_played=random.randrange(0, 50))
                self.stdout.write(self.style.SUCCESS(f'Player {username} created for team {team.name}'))

        # Create Games
        for _ in range(16):
            team1, team2 = random.sample(teams, 2)
            game = Game.objects.create(
                team1=team1,
                team2=team2,
                team1_score=random.randint(50, 150),
                team2_score=random.randint(50, 150),
                date=fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
            )
            self.stdout.write(self.style.SUCCESS(f'Game created between {team1.name} and {team2.name}'))

        self.stdout.write(self.style.SUCCESS('Fake data generation completed'))
