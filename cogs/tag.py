import discord
import sys 
import os
import re
from discord.ext import commands
from discord import app_commands
from urllib.parse import urlparse, ParseResult
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import embed
from report import Report
from fflogs import FFLogsSession

load_dotenv(".env")

class FFLogsReportError(Exception):
    """Raise an exception upon receiving invalid report link."""

class tag(commands.Cog):
  FFLOGS_CLIENT_ID = os.environ.get("FFLOGS_CLIENT_ID")
  FFLOGS_CLIENT_SECRET = os.environ.get("FFLOGS_CLIENT_SECRET")

  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  def isValidFFLogsPrefix(self, 
                          parsedLink: ParseResult) -> bool:
    """Tests link and return True if is an FFLogs Report link."""
    return (parsedLink.netloc.startswith("www.fflogs.com") and
            parsedLink.path.startswith("/reports/"))

  def getFFLogReportCode(self, 
                         parsedLink: ParseResult) -> str:
    """Extracts url path for FFLogs Report code."""
    if not self.isValidFFLogsPrefix(parsedLink): 
      raise FFLogsReportError("Not a valid FFLogs report.")
    return parsedLink.path.split("/")[2]

  def queriedFight(self,
                   parsedLink: ParseResult) -> int:
    fightQuery = re.search(r"fight=(\d+|last)", parsedLink.geturl()).groups()[0]
    if fightQuery == "last": return -1
    elif fightQuery.isnumeric(): return int(fightQuery)
    else: return 0

  @app_commands.command(
    name="tag",
    description="Automatically generates a summary for a linked FFLogs report."
  )
  @app_commands.describe(link="A link to an FFLogs report.")
  @app_commands.describe(description="Optional. Add further notes to a report.")
  async def tag(
      self, 
      interaction:discord.Interaction,
      link: str, 
      description: str = ""
  ) -> None:
    await interaction.response.defer()
    try:
      linkParse = urlparse(link)
      self.FFLogsSession = FFLogsSession(self.FFLOGS_CLIENT_ID, 
                                          self.FFLOGS_CLIENT_SECRET)
      self.logReportCode = self.getFFLogReportCode(linkParse)
      self.reportData = self.FFLogsSession.getReportData(self.logReportCode)
      self.report = Report(self.reportData)
      
      if self.queriedFight(linkParse):
        self.reportEmbed = self.report.grabFightEmbedByID(
          self.queriedFight(linkParse), 
          description
          )
      else:
        self.reportEmbed = self.report.toEmbed(link, description)
        # self.reportEmbed = embed.generateEmbed(self.reportData, link, description)
      
      await interaction.followup.send(embed = self.reportEmbed)
    except Exception as exc:
      await interaction.followup.send(exc, ephemeral=True)

async def setup(bot: commands.Bot):
  await bot.add_cog(tag(bot))