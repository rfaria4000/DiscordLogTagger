import functools
import discord
import math
from typing import Optional, Union
from enum import IntEnum
from dataclasses import dataclass
from data import jobinfo, parses

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
               rankingData: Optional[dict] = None):
    self.fightData: dict = fightData
    self.actorData: list = actorData
    self.rankingData: dict = rankingData if rankingData is not None else {}
    self.partyMembers: list[PartyMember] = []
    for key, value in self.fightData.items():
      setattr(self, key, value)
    self._unpackPartyMembers()

  def _unpackPartyMembers(self) -> None:
    """
     Populates self.partyMembers with a list of PartyMembers sorted by job 
     priority.
    """
    for actorID in self.friendlyPlayers:
      player = next(actor for actor in self.actorData if actor["id"] == actorID)
      if player["subType"] == LIMIT_BREAK_NPC: continue
      
      parse = None
      if self.rankingData:
        for role in self.rankingData["roles"].values():
          playerParse = next((character for character in role["characters"] 
                             if character["name"] == player["name"]), 
                             None)
          if playerParse is not None: parse = playerParse["rankPercent"]
      
      self.partyMembers.append(PartyMember(player["name"],
                                           player["subType"],
                                           parse))
    
    self.partyMembers.sort(key = lambda player: 
                           jobinfo.emojiDict[player.job].priority)

  def __str__(self):
    return (
      f"Overview for fight {self.id}:\n"
      f"  Name: {self.name}\n"
      f"  Difficulty: {self.fightTier}\n"
      f"  Status: {self.completionStatus}"
    )

  def __eq__(self, other):
    pass

  # for fights within the same category of ult/savage etc, it seems
  # bigger number for encounterID is more recent
  def __gt__(self, other):
    pass

  @property
  def fightTier(self) -> int:
    """
    Returns an int (enum) corresponding to the tier of a fight.\n
    0 - Unranked | 1 - Ranked | 2 - Savage | 3 - Ultimate
    """
    if self.lastPhase > 0: 
      return FightTier.ULTIMATE
    elif self.difficulty == 101:
      return FightTier.SAVAGE
    elif self.rankingData: 
      return FightTier.RANKED
    else: 
      return FightTier.UNRANKED
    
  @property
  def secondsElapsed(self) -> int:
    """
     Returns the fight duration in seconds. If a string representation is
     needed, use `timeElapsed()` instead.
    """
    return math.floor((self.endTime - self.startTime) / 1000)

  @property
  def timeElapsed(self) -> str:
    """
     Returns the fight duration as a string in 'XX:YY' format. If seconds are
     needed for comparison purposes, use `secondsElapsed()` instead.
    """
    return f"{self.secondsElapsed//60}:{self.secondsElapsed%60}"

  @property
  def completionStatus(self) -> str:
    """Returns a string summarizing a pull's completion rate."""
    if self.kill: return f"Clear in {self.timeElapsed}"
    if self.fightTier() == FightTier.ULTIMATE:
      return f"Phase {self.lastPhase} - {self.bossPercentage}% remaining"
    return f"{self.bossPercentage}% remaining"

  @property
  def bestParse(self) -> Optional[int]:
    """
    Returns the best parse out of any player on this fight. If there is no
    ranking associated with this fight, returns -1. If the fight was not
    cleared, returns None.
    """
    if not self.kill: return None
    if not self.rankingData: return -1
    return max([character.parse for character in self.partyMembers])

  @property
  def emoji(self):
    """
    Returns an emoji representing the state of the fight. If the fight is
    ranked, it will return an emoji whose color matches that of the best parse
    of the players that participated in this pull.
    """
    if not self.kill: return parses.PULL_EMOJIS[parses.Pull.WIPE]
    return parses.PULL_EMOJIS[parses.parseToIndex(self.bestParse)]

  @property
  def color(self):
    """
    Returns a hexcode representing the state of the fight. If the fight is
    ranked, the color will indicate the best parse of any participating player.
    Otherwise, it will be red for a wipe and mint green for a clear.
    """
    if not self.kill: return parses.PULL_HEXCODES[parses.Pull.WIPE]
    return parses.PULL_HEXCODES[parses.parseToIndex(self.bestParse)]

  @property
  def thumbnailURL(self) -> str:
    """Returns a link to the image associated with the encounter."""
    url = "https://assets.rpglogs.com/img/ff/bosses/{0}-icon.jpg"
    return url.format(self.encounterID)

  def displayPartyMembers(self) -> str:
    """
    Returns a string containing all party members and emojis representing their
    respective jobs.
    """
    memberString = [f"{jobinfo.emojiDict[member.job].emoji} {member.name}" 
                         for member in self.partyMembers]
    return "\n".join(memberString)

  def displayPartyParses(self) -> str:
    """
    Returns a string containing the emojis of each party member, an emoji
    representing their parse, and their actual parse.
    """
    emojiString = [(f"{jobinfo.emojiDict[member.job].emoji} "
                    f"{parses.PULL_EMOJIS[parses.parseToIndex(member.parse)]} " 
                    f"{member.parse}") 
                    for member in self.partyMembers]
    return "\n".join(emojiString)

  def toEmbed(self) -> discord.Embed:
    """
    Returns a Discord Embed representing the fight. It does not contain any meta
    data such as the author of the report, a link to the report, or when
    the fight occured.
    """
    fightEmbed = discord.Embed()
    fightEmbed.title = f"🔸 {self.name}"
    fightEmbed.set_thumbnail(url=self.thumbnailURL)
    fightEmbed.color = self.color
    
    fightEmbed.add_field(name="Status", 
                         value=self.completionStatus, 
                         inline=False)
    fightEmbed.add_field(name="Party", 
                         value=self.displayPartyMembers(),
                         inline=True)
    if self.rankingData:
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
  print(fightTen.toEmbed().to_dict())