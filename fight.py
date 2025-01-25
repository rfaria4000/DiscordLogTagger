import functools
import discord
import math
from typing import Optional, Union
from enum import IntEnum
from dataclasses import dataclass
from data import jobinfo

LIMIT_BREAK_NPC = "LimitBreak"
FIELD_DENOTING_COMBINED_PARSE = "name_2"

class FightTier(IntEnum):
  UNRANKED = 0
  RANKED = 1 #Extremes and Normal Raids
  SAVAGE = 2
  ULTIMATE = 3

@dataclass
class PartyMember():
  name: str
  job: str
  parse: int = None

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
    self.partyMembers: list[PartyMember] = []
    for key, value in self.fightData.items():
      setattr(self, key, value)
    self._unpackPartyMembers()

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

  def _unpackPartyMembers(self) -> None:
    """
     Populates self.partyMembers with a list of PartyMembers sorted by job 
     priority.
    """
    for actorID in self.friendlyPlayers:
      player = next(actor for actor in self.actorData if actor["id"] == actorID)
      if player["subType"] == LIMIT_BREAK_NPC: continue
      
      parse = None
      if self.rankingData is not None:
        for role in self.rankingData["roles"].values():
          playerParse = next((character for character in role["characters"] 
                             if character["name"] == player["name"]), 
                             None)
          if playerParse is not None: 
            if FIELD_DENOTING_COMBINED_PARSE in playerParse: break
            parse = playerParse["rankPercent"]
      
      self.partyMembers.append(PartyMember(player["name"],
                                           player["subType"],
                                           parse))
    
    self.partyMembers.sort(key = lambda player: 
                           jobinfo.emojiDict[player.job].priority)

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
    fightEmbed.add_field(name="Status", 
                         value=self.completionStatus(), 
                         inline=False)
    fightEmbed.add_field(name="Party", 
                         value=self.displayPartyMembers(),
                         inline=True)
    if self.rankingData is not None:
      fightEmbed.add_field(name="Parses", 
                           value=self.displayPartyParses(),
                           inline=True)
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
  print(fightTen.partyMembers)