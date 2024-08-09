import discord, os
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv

load_dotenv(".env")
MY_GUILD_ID = discord.Object(os.getenv("DISCORD_GUILD_ID"))

class sync(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  
  # NOTE: not an app command
  @commands.command(
      name="sync",
      description="Synchronizes slash commands."
  )
  @commands.is_owner()
  async def sync(self, context: Context) -> None:
    print("called sync command")
    await context.bot.tree.sync()
    embed = discord.Embed(
      description="Successfully created, restart Discord to see updates.",
      color=0x3EB489
    )
    await context.reply(embed=embed, mention_author=False)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(sync(bot))