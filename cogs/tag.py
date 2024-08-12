import discord
from discord.ext import commands
from discord import app_commands

class tag(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

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
    await interaction.response.send_message(content="Tag called")

async def setup(bot: commands.Bot):
  await bot.add_cog(tag(bot))