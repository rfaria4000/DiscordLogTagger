import functools
import discord
import math
from typing import Optional, Union
from enum import IntEnum

class FightTier(IntEnum):
  UNRANKED = 0
  RANKED = 1 #Extremes and Normal Raids
  SAVAGE = 2
  ULTIMATE = 3

@functools.total_ordering
class Fight:
  """
  Represents a fight, or a more commonly known as a pull of a duty.
  """
  def __init__(self, 
               fightData: dict, 
               actorData: list, 
               rankingData: dict = None):
    self.fightData: dict = fightData
    self.actorData: list = actorData
    self.rankingData: dict = rankingData
    for key, value in self.fightData.items():
      setattr(self, key, value)

  def fightTier(self) -> int:
    """
    Returns an int (enum) corresponding to the tier of a fight.\n
    0 - Unranked | 1 - Ranked | 2 - Savage | 3 - Ultimate
    """
    if self.lastPhase > 0: 
      return FightTier.ULTIMATE
    elif self.difficulty == 101:
      return FightTier.SAVAGE
    elif self.rankingData is not None: 
      return FightTier.RANKED
    else: 
      return FightTier.UNRANKED
    
  def secondsElapsed(self) -> int:
    """
     Returns the fight duration in seconds. If a string representation is
     needed, use `timeElapsed()` instead.
    """
    return math.floor((self.endTime - self.startTime) / 1000)

  def timeElapsed(self) -> str:
    """
     Returns the fight duration as a string in 'XX:YY' format. If seconds are
     needed for comparison purposes, use `secondsElapsed()` instead.
    """
    return f"{self.secondsElapsed()//60}:{self.secondsElapsed()%60}"

  def completionStatus(self) -> str:
    """Returns a string summarizing a pull's completion rate."""
    if self.kill: return f"Clear in {self.timeElapsed()}"
    if self.fightTier() == FightTier.ULTIMATE:
      return f"Phase {self.lastPhase} - {self.bossPercentage}% remaining"
    return f"{self.bossPercentage}% remaining"

  def __str__(self):
    return (
      f"Overview for fight {self.id}:\n"
      f"  Name: {self.name}\n"
      f"  Difficulty: {self.fightTier()}\n"
      f"  Status: {self.completionStatus()}"
    )

  def __eq__(self, other):
    pass

  # for fights within the same category of ult/savage etc, it seems
  # bigger number for encounterID is more recent
  def __gt__(self, other):
    pass

  def toEmoji(self):
    pass

  def toColor(self):
    pass

  def displayPartyMembers(self) -> str:
    pass

  def displayPartyParses(self) -> str:
    pass

  def thumbnailURL(self) -> str:
    """Returns a link to the image associated with the encounter."""
    url = "https://assets.rpglogs.com/img/ff/bosses/{0}-icon.jpg"
    return url.format(self.encounterID)

  def toEmbed(self) -> discord.Embed:
    fightEmbed = discord.Embed()
    fightEmbed.title = f"🔸 {self.name}"
    fightEmbed.set_thumbnail(url=self.thumbnailURL())
    fightEmbed.color = self.toColor()
    fightEmbed.add_field(name="Status", value=self.completionStatus())
    return fightEmbed

if __name__ == "__main__":
  import json, os

  dir = os.path.dirname(__file__)
  mockReportData = None
  with open(os.path.join(dir, "tests/test_data/extreme.json"), "r") as f:
    mockReportData = json.load(f)
  
  mockFightData = mockReportData["data"]["reportData"]["report"]["fights"][9]
  mockActorData = mockReportData["data"]["reportData"]["report"]["masterData"]["actors"]
  mockRankingData = mockReportData["data"]["reportData"]["report"]["rankings"]["data"][0] #fight id 10
  fightTen = Fight(mockFightData, mockActorData, mockRankingData)
  print(fightTen.toEmbed())