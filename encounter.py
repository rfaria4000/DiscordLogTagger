import discord
import functools
from typing import Optional
from fight import Fight

@functools.total_ordering
class Encounter:
  def __init__(self,
               encounterID: int = -1,
               fightList: Optional[list[Fight]] = None):
    self.encounterID = encounterID
    # http://docs.python.org/reference/compound_stmts.html#function-definitions
    # For future reference as to why the default parameter shouldn't be a 
    # mutable object (empty list in this case)
    self.fightList = fightList if fightList is not None else []

  def __str__(self):
    return (
      f"Overview for encounter {self.encounterID}:\n"
      f"  Name: {self.name}\n"
      f"  Pulls: {self.pulls}\n"
    )
  
  def __eq__(self, other):
    if not isinstance(other, Encounter): return NotImplemented
    
    return ((self.encounterID == other.encounterID) and
            (self.fightList == other.fightList) and
            (self.url == other.url))

  def __gt__(self, other):
    if not isinstance(other, Encounter): return NotImplemented

    return self.bestFight > other.bestFight

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
  
  @property
  def bestFight(self) -> Fight:
    return max(self.fightList)

  def addFight(self, fight: Fight) -> None:
    # verify encounterID matches
    # add it to list
    # TODO: Replace exception with more graceful behavior 
    if fight.encounterID != self.encounterID: raise Exception
    self.fightList.append(fight)

  def toEmbed(self, 
              link: str = None,
              description: str = None) -> discord.Embed:
    """
    Returns a Discord Embed representing the Encounter. Like the Fight toEmbed,
    it does not include any meta data about the fight.

    Args
    ---
      link: `str`
        A link to the report used to link to the best fight. Must not contain
        any queries.
    """
    if self.pulls == 1: return self.fightList[0].toEmbed(description)

    encounterEmbed = discord.Embed()
    encounterEmbed.title = f"🔷 {self.name}"
    encounterEmbed.set_thumbnail(url=self.bestFight.thumbnailURL)
    
    encounterEmbed.add_field(name = "Pulls",
                             value = str(self.pulls),
                             inline = False)
    
    bestPullValue = f"{self.bestFight.completionStatus}"
    if link is not None:
      bestPullValue = (f"[{bestPullValue}]"
                       f"({link}?fight={self.bestFight.id})")
    encounterEmbed.add_field(name = "Best Pull",
                              value = bestPullValue,
                              inline = False)
    return encounterEmbed