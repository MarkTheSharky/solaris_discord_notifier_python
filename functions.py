from replit import db
import requests

def get_galaxy_data(game_id):
  root = 'https://api.solaris.games/api/game/' + game_id + '/galaxy'
  payload = requests.get(root)
  return payload.json()

def set_starting_game_data(game_id):
  payload = get_galaxy_data(game_id)
  db[game_id] = {
      "current_tick": payload["state"]["tick"]
  }

def check_if_game_database_exists_or_set_it(game_id):
  if game_id in db:
    print('Game already in database')
  else:
    set_starting_game_data(game_id)
    print('Starting game data set')

def send_starting_message():
  return 'This is a starting message'