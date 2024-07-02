import os
from dotenv import load_dotenv

import discord

load_dotenv(".env")
DISCORD_TOKEN = os.environ.get("ENV_DISCORD_TOKEN")
DISCORD_GUILD = os.environ.get("ENV_DISCORD_GUILD_NAME")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=DISCORD_GUILD)

    print(f'{client.user} has connnected to Discord')
    print(f'{guild.name}: has id:{guild.id}')

@client.event
async def on_message(message):
    print(f"Message sent: {message.content}")
    if message.author == client.user:
        return
    
    if message.content == "Test Log Bot":
        embedVar = discord.Embed(title="The Unending Coil of Bahamut - June 18, 2024",color=0xffd1dc)
        embedVar.add_field(name="Pulls", value="13")
        # embedVar.add_field(name="Date", value="Today", inline=True)
        embedVar.add_field(name="Clear?", value="Yes")
        embedVar.add_field(name="Furthest phase", value="P4")
        # embedVar.add_field(name="View report", value="[View report](https://www.fflogs.com/reports/7Myb4A6dDq1HnWvc)")
        embedVar.url = "https://www.fflogs.com/reports/7Myb4A6dDq1HnWvc"
        # embedVar.add_field(name="Link to report", value="https://www.fflogs.com/reports/7Myb4A6dDq1HnWvc")
        
        await message.channel.send(embed=embedVar)

# @client.event
# async def on_message(message):
#   if message.author == client.user:
#     return
  
#   if message.content.startsWith('$hello'):
#     await message.channel.send('Hello!')

client.run(DISCORD_TOKEN)