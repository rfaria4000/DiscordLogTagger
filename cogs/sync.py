import discord, os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(".env")

MY_GUILD_ID = discord.Object(os.getenv("DISCORD_GUILD_ID"))

class sync(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  
  @app_commands.command(
      name="sync",
      description="Sync the command tree globally."
  )
  @app_commands.guilds(MY_GUILD_ID)
  @commands.is_owner()
  async def sync(self, interaction: discord.Interaction) -> None:
    print("called sync command")
    await interaction.response.send_message("Successfully created")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(sync(bot))