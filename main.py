import os
import requests
import discord
from discord.ext import commands, tasks
from keep_alive import keep_alive


TOKEN = os.environ['TOKEN']
GUILD = os.environ['GUILD']
GAME_ID = os.environ['GAME_ID']

current_tick = 0

def get_galaxy_data(game_id):
  root = 'https://api.solaris.games/api/game/' + GAME_ID + '/galaxy'
  payload = requests.get(root)
  return payload.json()

client = discord.Client()
@client.event
async def on_ready():
    print(f'{client.user.name} is connected to the server.')
    post_when_new_turn.start(GAME_ID)

@tasks.loop(minutes=5)
async def post_when_new_turn(game_id):
  global current_tick
  new_tick = get_galaxy_data(game_id)['state']['tick']
  if new_tick > current_tick:
    current_tick = new_tick
    channel = client.get_channel(866734536052965406)
    await channel.send('New turn! We are now on tick ' + str(current_tick))
    print('Sent new tick ' + str(new_tick) + ' to server.')
  else:
    pass

keep_alive()
client.run(TOKEN)