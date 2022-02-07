import functions
import os
import discord
from discord.ext import tasks
from keep_alive import keep_alive
from replit import db

# Set environment variables
TOKEN = os.environ['TOKEN']
GUILD = os.environ['DISCORD_GUILD']
DISCORD_CHANNEL_ID = os.environ['DISCORD_CHANNEL_ID']
GAME_ID = os.environ['GAME_ID']

# Check if game exists in database already or make it
functions.check_if_game_database_exists_or_set_it(GAME_ID)

# Assign the Discord library to variable
client = discord.Client()

# Start the Discord client
@client.event
async def on_ready():
  print(f'{client.user.name} is connected to the server.')

# Check to see if the game has started and send a welcome message
  if db[GAME_ID]["current_tick"] == 0:
    print("Ran 'if current_tick == 0:'")
    channel = client.get_channel(784061864312700939)
    await channel.send(functions.send_starting_message())
    db[GAME_ID]["current_tick"] = 1

  post_when_new_turn.start(GAME_ID)


# Assign functions to check for game status and send message on Discord
@tasks.loop(minutes=5)
async def post_when_new_turn(game_id):
  new_tick = functions.get_game_state(game_id)['tick']
  current_tick = db[GAME_ID]["current_tick"]
  # print("Current tick is: " + str(current_tick))

# Check saved game state with current game state and send message if theres a new turn
  if new_tick > current_tick:
    print("Ran 'elif new_tick > current_tick:'")
    db[GAME_ID]["current_tick"] = new_tick
    channel = client.get_channel(784061864312700939)
    await channel.send('New turn! We are now on tick ' + str(db[GAME_ID]["current_tick"]))
    print('Sent new tick ' + str(db[GAME_ID]["current_tick"]) + ' to server.')

keep_alive()
client.run(TOKEN)