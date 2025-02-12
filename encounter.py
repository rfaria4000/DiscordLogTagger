import discord
from typing import Optional
from fight import Fight

class Encounter:
  def __init__(self,
               encounterID: int = -1,
               fightList: Optional[list[Fight]] = None, 
               url: str = ""):
    self.encounterID = encounterID
    # http://docs.python.org/reference/compound_stmts.html#function-definitions
    # For future reference as to why the default parameter shouldn't be a 
    # mutable object (empty list in this case)
    self.fightList = fightList if fightList is not None else []
    self.url = url

  def __str__(self):
    return (
      f"Overview for encounter {self.encounterID}:\n"
      f"  Name: {self.name}\n"
      f"  Pulls: {self.pulls}\n"
    )

  @classmethod
  def fromFight(cls, fight: Fight, url: str = None):
    return cls([fight], url)

  @property
  def pulls(self) -> int:
    return len(self.fightList)
  
  @property
  def name(self) -> str:
    if not self.fightList: return "No fights added to encounter."
    return self.fightList[0].name

  def addFight(self, fight: Fight) -> None:
    # verify encounterID matches
    # add it to list
    # TODO: Replace exception with more graceful behavior 
    if fight.encounterID != self.encounterID: raise Exception
    self.fightList.append(fight)

  def toEmbed(self) -> discord.Embed:
    if self.pulls == 1: return self.fightList[0].toEmbed()
    
    bestFight: Fight = max(self.fightList)

    encounterEmbed = discord.Embed()
    encounterEmbed.title = f"🔷 {self.name}"
    encounterEmbed.set_thumbnail(url=bestFight.thumbnailURL)
    
    encounterEmbed.add_field(name="Pulls",
                             value=str(self.pulls),
                             inline=False)
    return encounterEmbed