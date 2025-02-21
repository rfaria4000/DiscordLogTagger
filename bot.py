import os
import discord

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
    for file in os.listdir('./cogs'):
      if file.endswith(".py"):
        try:
          await self.load_extension(f"cogs.{file[:-3]}")
          print(f"Successfully loaded {file}")
        except Exception as e:
          print(f"Failed to load {file}")

  async def on_ready(self):
    print(f'{self.user} has connected to Discord!')

if __name__ == "__main__":
  bot = DiscordBot()
  bot.run(os.getenv("DISCORD_TOKEN"))