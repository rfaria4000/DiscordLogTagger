import discord
# from typing import Optional
from fight import Fight

class Encounter:
  def __init__(self, fightList: list[Fight] = [], 
               url: str = ""):
    self.fightList = fightList
    self.url = url

  @classmethod
  def fromFight(cls, fight: Fight, url: str = None):
    return cls([fight], url)

  @property
  def pulls(self) -> int:
    return len(self.fightList)
  
  @property
  def name(self) -> str:
    if not self.fightList: return "No fights added to encounter."
    return next(self.fightList).name
  
  @property
  def encounterID(self) -> int:
    if not self.fightList: return -1
    return next(self.fightList).encounterID

  def addFight(self, fight: Fight) -> None:
    # verify encounterID matches
    # add it to list
    pass

  def toEmbed(self) -> discord.Embed:
    bestFight: Fight = max(self.fightList)

    encounterEmbed = discord.Embed()
    encounterEmbed.title = f"🔷 {self.name}"
    encounterEmbed.set_thumbnail(url=bestFight.thumbnailURL)
    
    encounterEmbed.add_field(name="Pulls",
                             value=str(self.pulls),
                             inline=False)
    return encounterEmbed