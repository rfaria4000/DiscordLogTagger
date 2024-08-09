import os, discord

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv(".env")

intents = discord.Intents.default()
intents.message_content = True

class DiscordBot(commands.Bot):
  def __init__(self) -> None:
    super().__init__(
      command_prefix="$",
      intents=intents
    )
    pass
  
  async def setup_hook(self):
    await self.load_extension(f"cogs.test")
    await self.load_extension(f"cogs.sync")
    await bot.tree.sync(guild=discord.Object(os.getenv("DISCORD_GUILD_ID")))
    # await bot.tree.sync()

  async def on_ready(self):
    print(f'{self.user} has connected to Discord!')

if __name__ == "__main__":
  bot = DiscordBot()
  bot.run(os.getenv("DISCORD_TOKEN"))