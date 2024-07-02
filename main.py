import os
from dotenv import load_dotenv

import discord

load_dotenv(".env")
DISCORD_TOKEN = os.environ.get("ENV_DISCORD_TOKEN")

intents = discord.Intents.default()
# intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print(f'{client.user} has connnected to Discord')

# @client.event
# async def on_message(message):
#   if message.author == client.user:
#     return
  
#   if message.content.startsWith('$hello'):
#     await message.channel.send('Hello!')

client.run(DISCORD_TOKEN)