import os
import discord

from dotenv import load_dotenv
from discord import app_commands
from urllib.parse import urlparse
from fflogs import FFLogsSession
import embed

class FFLogsReportError(Exception):
    """Raise an exception upon receiving invalid report link."""

load_dotenv(".env")
DISCORD_TOKEN = os.environ.get("ENV_DISCORD_TOKEN")
DISCORD_GUILD_NAME = os.environ.get("ENV_DISCORD_GUILD_NAME")
DISCORD_GUILD_ID = os.environ.get("ENV_DISCORD_GUILD_ID")
FFLOGS_CLIENT_ID = os.environ.get("ENV_FFLOGS_CLIENT_ID")
FFLOGS_CLIENT_SECRET = os.environ.get("ENV_FFLOGS_CLIENT_SECRET")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

ffLogsSession = FFLogsSession(FFLOGS_CLIENT_ID, FFLOGS_CLIENT_SECRET)

def isValidFFLogsPrefix(link: str) -> bool:
    """Tests link and return True if is an FFLogs Report link."""
    fflogsEndpoint = "https://www.fflogs.com/reports/"
    return link.startswith(fflogsEndpoint)

def getFFLogReportCode(link:str) -> str:
    """Extracts url path for FFLogs Report code."""
    if not isValidFFLogsPrefix(link): raise FFLogsReportError("Not a valid FFLogs report.")
    parsedLink = urlparse(link)
    return parsedLink.path.split("/")[2]

@tree.command(
  name="tag",
  description="Automatically generates a descripiton for a linked FFLogs report.",
  guild=discord.Object(id=DISCORD_GUILD_ID)
)
# @app_commands.rename(link="displayVariableNameHere")
@app_commands.describe(link="Link to an FFLogs report.")
@app_commands.describe(description="Add further context to the report.")
async def tag(interaction, link: str, description:str =""):
    try:
        logReportCode = getFFLogReportCode(link)
        reportData = ffLogsSession.getReportData(logReportCode)
        reportEmbed = embed.generateEmbedFromReport(reportData, link, description)
        await interaction.response.send_message(embed = reportEmbed)
    except FFLogsReportError as exc:
      await interaction.response.send_message(exc, ephemeral=True)
    except embed.ReportDataError as exc:
        await interaction.response.send_message(exc, ephemeral=True)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=DISCORD_GUILD_NAME)

    print(f'{client.user} has connnected to Discord')
    print(f'{guild.name}: has id:{guild.id}')
    # authorizeFFLogs(FFLOGS_CLIENT_ID,FFLOGS_CLIENT_SECRET)
    await tree.sync(guild=discord.Object(id=guild.id))

@client.event
async def on_message(message):
    print(f"Message sent: {message.content}")
    if message.author == client.user:
        return
    
    if message.content == "Test Log Bot":
        embedVar = discord.Embed(title="The Unending Coil of Bahamut - June 18, 2024",color=0xffd1dc)
        embedVar.description = "Testing out what a description looks like"
        embedVar.set_thumbnail(url="https://assets.rpglogs.com/img/ff/bosses/1060-icon.jpg")
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
if __name__ == "__main__":
  client.run(DISCORD_TOKEN)