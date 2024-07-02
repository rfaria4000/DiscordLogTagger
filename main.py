import os
from dotenv import load_dotenv

import discord

load_dotenv(".env")
DISCORD_TOKEN = os.environ.get("ENV_DISCORD_TOKEN")
DISCORD_GUILD = os.environ.get("ENV_DISCORD_GUILD_NAME")

intents = discord.Intents.default()
# intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  
  for guild in client.guilds:
    if guild == DISCORD_GUILD:
      break

    print(f'{client.user} has connnected to Discord')
    print(f'{guild.name}: has id:{guild.id}')


# @client.event
# async def on_message(message):
#   if message.author == client.user:
#     return
  
#   if message.content.startsWith('$hello'):
#     await message.channel.send('Hello!')

client.run(DISCORD_TOKEN)