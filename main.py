import os
import discord

from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from urllib.parse import urlparse
from fflogs import FFLogsSession

import embed

class FFLogsReportError(Exception):
    """Raise an exception upon receiving invalid report link."""

load_dotenv(".env")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
DISCORD_GUILD_NAME = os.environ.get("DISCORD_GUILD_NAME")
DISCORD_GUILD_ID = os.environ.get("DISCORD_GUILD_ID")
FFLOGS_CLIENT_ID = os.environ.get("FFLOGS_CLIENT_ID")
FFLOGS_CLIENT_SECRET = os.environ.get("FFLOGS_CLIENT_SECRET")

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
  print(parsedLink)
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
  await interaction.response.defer()
  try:
      logReportCode = getFFLogReportCode(link)
      reportData = ffLogsSession.getReportData(logReportCode)
      # await interaction.response.send_message(content="test")
      reportEmbed = embed.generateEmbed(reportData, link, description)
      await interaction.followup.send(embed = reportEmbed)
  except FFLogsReportError as exc:
    await interaction.followup.send(exc, ephemeral=True)
  except embed.ReportDataError as exc:
    await interaction.followup.send(exc, ephemeral=True)

@client.event
async def on_ready():
  guild = discord.utils.get(client.guilds, name=DISCORD_GUILD_NAME)

  print(f'{client.user} has connnected to Discord')
  print(f'{guild.name}: has id:{guild.id}')
  # authorizeFFLogs(FFLOGS_CLIENT_ID,FFLOGS_CLIENT_SECRET)
  await tree.sync(guild=discord.Object(id=guild.id))
  


if __name__ == "__main__":
  client.run(DISCORD_TOKEN)