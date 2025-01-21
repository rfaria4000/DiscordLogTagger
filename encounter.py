import discord
from typing import Optional

class Encounter:
  def __init__(self, fightList, url: str):
    pass

  def verify_fights(self):
    pass

  def to_embed(self, partialEmbed: Optional[discord.Embed]) -> discord.Embed:
    returnEmbed = partialEmbed if partialEmbed else discord.Embed()
    pass