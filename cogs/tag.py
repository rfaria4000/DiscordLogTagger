import discord, sys, os
from discord.ext import commands
from discord import app_commands
from urllib.parse import urlparse
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

  def isValidFFLogsPrefix(self, link: str) -> bool:
    """Tests link and return True if is an FFLogs Report link."""
    fflogsEndpoint = "https://www.fflogs.com/reports/"
    return link.startswith(fflogsEndpoint)

  def getFFLogReportCode(self, link:str) -> str:
    """Extracts url path for FFLogs Report code."""
    if not self.isValidFFLogsPrefix(link): 
      raise FFLogsReportError("Not a valid FFLogs report.")
    parsedLink = urlparse(link)
    print(parsedLink)
    return parsedLink.path.split("/")[2]

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
      self.FFLogsSession = FFLogsSession(self.FFLOGS_CLIENT_ID, 
                                         self.FFLOGS_CLIENT_SECRET)
      self.logReportCode = self.getFFLogReportCode(link)
      self.reportData = self.FFLogsSession.getReportData(self.logReportCode)
      self.report = Report(self.reportData)
      self.reportEmbed = self.report.toEmbed(link, description)
      # self.reportEmbed = embed.generateEmbed(self.reportData, link, description)
      await interaction.followup.send(embed = self.reportEmbed)
    except Exception as exc:
      await interaction.followup.send(exc, ephemeral=True)

async def setup(bot: commands.Bot):
  await bot.add_cog(tag(bot))