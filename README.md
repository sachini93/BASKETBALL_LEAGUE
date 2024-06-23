# BASKETBALL_LEAGUE

##Project Overview
This is a management system designed for a Basketball tournament, that will help stakeholders identified in the tournament to manage user data, tracking of game details etc..

**The main user roles involved in the system are:**
- League Admin
- Player
- Coach
  
**Features:**
- User management: Manage user roles, User login, Role-based access management, Track user logins, time spent on the site, and current online status, Create/Update/Get/Delete user data.
- Team management: Create/Update/Get/Delete teams, Assign Teams with Players, and coaches, View team statistics (ex: team average score, Players within the team who are inside the 90th average score     
  percentile)
- Tournament management: Create/Update/Get/Delete Games between teams, Record and display game scores and winning teams, scoreboard
- Player management: Create/Update/Get/Delete Players, View player statistics (ex: average scores and participation)

## Installation
Follow these steps to set up the project on your local machine.

### Prerequisites
- Python 3.x
- Django 3.x or higher
- pip (Python package installer)

### Clone the Repository
- git clone https://github.com/sachini93/BASKETBALL_LEAGUE.git
- cd BASKETBALL_LEAGUE/league_management

### Create a Virtual Environment
- python3 -m venv env
- source env/bin/activate  (# On Windows use env\Scripts\activate)

### Install Dependencies
- pip install -r requirements.txt
  
### Apply migrations
- python manage.py makemigrations
- python manage.py migrate

### Create a super user
- python manage.py createsuperuser --username admin --email admin@example.com

### Run Server
- python manage.py runserver

## App Endpoints
- Navigate to 'http://127.0.0.1:8000/admin' and log in using the superuser credentials created earlier.
  ### User Authentication and obtain an authentication token:
  - POST /api/api-token-auth/
  ### Teams
  - GET /api/teams/: List all teams.
  - POST /api/teams/: Create a new team.
  - GET /api/teams/<id>/: Retrieve a team by ID.
  - PUT /api/teams/<id>/: Update a team by ID.
  - DELETE /api/teams/<id>/: Delete a team by ID.
 
  ### Players
  - GET /api/players/: List all players.
  - POST /api/players/: Create a new player.
  - GET /api/players/<id>/: Retrieve a player by ID.
  - PUT /api/players/<id>/: Update a player by ID.
  - DELETE /api/players/<id>/: Delete a player by ID.
 
  ### Games
  - GET /api/games/: List all games.
  - POST /api/games/: Create a new game.
  - GET /api/games/<id>/: Retrieve a game by ID.
  - PUT /api/games/<id>/: Update a game by ID.
  - DELETE /api/games/<id>/: Delete a game by ID.
 
## Management Commands
### Generate Fake Data
- To generate fake users, teams, players, and games use the custom management command:
 - python manage.py generate_fake_data
   
## Testing
### Integration Testing
- To run the integration test suite, execute the following command
 - python manage.py run_postman_tests

    

  





