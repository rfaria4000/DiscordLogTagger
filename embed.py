from discord import Embed
from datetime import datetime

from typing import Tuple, List
from urllib.parse import urlparse
from collections import namedtuple

import json, os, math

# Clear values for the purpose of comparing fights.
# Makes a clear of any fight with a rating higher than a pull off any fight.
CLEAR_RATING_BONUS = 3
CLEAR_THRESHOLD = 4

#TODO: Make a config file that will pull custom emojis for the bot

WIPE_HEXCODE = 0xff0000
UNRANKED_CLEAR_HEXCODE = 0xabebc6
PARSE_HEXCODES = [0x666666, 0x1eff00, 0x0070ff, 0xa335ee, 0xff8000, 0xe268a8, 0xe5cc80]

NO_CLEARS_EMOJI = "❌"
UNRANKED_CLEAR_EMOJI = "✅"
PARSE_EMOJIS = ["🩶", "💚", "💙", "💜", "🧡", "🩷", "💛"]

Ranking = namedtuple("Ranking", ["character", "parse", "job"])

class ReportDataError(Exception):
  """The received reportData is not correctly formatted or missing."""

def isFightUltimate(fight: dict) -> bool:
  """Returns whether a fight is an Ultimate."""
  return fight.get("lastPhase") > 0

def isFightSavage(fight: dict) -> bool:
  """Returns whether a fight is a Savage."""
  return fight.get("difficulty") == 101

def isFightExtreme(fight:dict, simplifiedRankings: dict) -> bool:
  """Returns whether a fight is an Extreme."""
  return fight["id"] in simplifiedRankings.keys()

def generateFightTier(fight:dict, simplifiedRankings: dict) -> int:
  """
  Returns an int corresponding to the tier of a fight.

  A 3 indicates an Ultimate fight.
  A 2 indicates a Savage fight.
  A 1 indicates a ranked Extreme fight (only on kill).
  A 0 indicates an unranked Extreme or any other fight.
  """
  if isFightUltimate(fight): return 3
  if isFightSavage(fight): return 2
  if isFightExtreme(fight, simplifiedRankings): return 1
  return 0

def extractReportFields(reportData: dict) -> Tuple[List[object], str, List[object], List[object]]:
  """
  Extracts the list of actors, date, and list of fights from a report.
   
   Args:
    `reportData`: A dict representing a json object containing reportData.

  Returns:
    A tuple containing the list of actor objects, the date of the report in 
    "Month Day, Year" format, a list of fights, and a possibly empty list of 
    rankings.
  """
  flattenedReport = reportData.get("data").get("reportData").get("report")

  actorList = flattenedReport.get("masterData").get("actors")

  startTimeUNIX = flattenedReport.get("startTime")  // 1000 # millisecond precision

  fightsList = flattenedReport.get("fights")

  rankingsList = flattenedReport.get("rankings").get("data")

  return actorList, startTimeUNIX, fightsList, rankingsList

def simplifyRanking(ranking: dict) -> tuple:
  """Convert a ranking object into a tuple with fightIDs and list of player parses."""
  characterParseList = []
  for role in ranking["roles"].values():
     for player in role["characters"]:
        # Tanks and healers have a combined player field - this prunes that 
        if "name_2" in player: continue
        characterParseList.append(Ranking(player["name"], player["rankPercent"], player["class"]))
  return (ranking.get("fightID"), characterParseList)
  
def simplifyActor(actor: dict) -> list:
   """Convert a dict representing an actor to a list of id and name."""
   return actor.values()

def getFightDuration(fight: dict) -> int:
  return fight["endTime"] - fight["startTime"]

def compareFights(fightOne: dict, fightTwo: dict, simplifiedRankings: dict) -> dict:
  """
  Return the more salient of the two fights.

  Priority is, in order: clear (if above tier 0), fight difficulty, fight duration.
  For right now, fights with different names in the same tier will prioritize longer fights.
  """

  fightOneRating = generateFightTier(fightOne, simplifiedRankings)
  fightTwoRating = generateFightTier(fightTwo, simplifiedRankings)

  if fightOneRating and fightOne["kill"]: fightOneRating += CLEAR_RATING_BONUS
  if fightTwoRating and fightTwo["kill"]: fightTwoRating += CLEAR_RATING_BONUS

  if fightOneRating != fightTwoRating: 
    return fightOne if fightOneRating > fightTwoRating else fightTwo
  
  if fightOneRating < CLEAR_THRESHOLD:
    return fightOne if fightOne["fightPercentage"] < fightTwo["fightPercentage"] else fightTwo

  isFightOneShorter = getFightDuration(fightOne) < getFightDuration(fightTwo)

  if fightOne["name"] == fightTwo["name"]:
    return fightOne if isFightOneShorter else fightTwo
  else:
    return fightTwo if isFightOneShorter else fightOne

def reduceFights(fights: dict, simplifiedRankings: dict) -> dict:
  """Converts list of fight objects into a dict of unique fights with aggregate data."""
  uniqueFightDict = {}
  for fight in fights:
    encounterID = fight["encounterID"]

    if not encounterID in uniqueFightDict.keys():
      uniqueFightDict[encounterID] = {
         "name": fight["name"],
         "pullCount": 1,
         "clearPulls": [],
         "bestPull": fight,
         "fightTier": generateFightTier(fight, simplifiedRankings),
         "bestParse": None
      }
      continue
    
    uniqueFight = uniqueFightDict[encounterID]
    uniqueFight["pullCount"] += 1
    
    if fight['kill']: 
      uniqueFight["clearPulls"].append(fight["id"])
      uniqueFight["fightTier"] = generateFightTier(fight, simplifiedRankings)
    
    uniqueFight["bestPull"] = compareFights(fight, 
                                            uniqueFight["bestPull"],
                                            simplifiedRankings)
  return uniqueFightDict

def chooseHighlightFight(simplifiedFights: dict) -> int:
  """Returns the highlight fight for the sake of thumbnails."""
  pass

def generateRankingColorIndex(parse: int) -> int:
  """Return an index 0-6 for a list of possible outputs based on a parse."""
  # Ranges can be found here: 
  # https://www.archon.gg/ffxiv/articles/help/rankings-and-parses
  if parse < 25: return 0
  elif parse < 50: return 1
  elif parse < 75: return 2
  elif parse < 95: return 3
  elif parse < 99: return 4
  elif parse == 99: return 5
  else: return 6

# TODO: Think about multiFight embed colors 
def generateEmbedColor(fight: dict, rankings: dict):
  print(rankings)
  """Generate a hex code for an Embed based on a fight."""
  if not fight["kill"]: return WIPE_HEXCODE #red

  bestParse = 0
  if fight["id"] in rankings:
    for ranking in rankings[fight["id"]]:
      bestParse = max(bestParse, ranking.parse) 
  else: return UNRANKED_CLEAR_HEXCODE #mint green
  
  return PARSE_HEXCODES[generateRankingColorIndex(bestParse)]

def generateClearEmoji(fightID: dict, rankings:dict) -> str:
  """Generate an emoji based on a cleared fights."""
  if not fightID in rankings: return UNRANKED_CLEAR_EMOJI

  bestParse = 0
  for ranking in rankings[fightID]:
    bestParse = max(bestParse, ranking.parse) 

  return PARSE_EMOJIS[generateRankingColorIndex(bestParse)]

def generateImageURL(encounterID: dict) -> str:
  """Generate a URL to a thumbnail based on the fight."""
  return f"https://assets.rpglogs.com/img/ff/bosses/{encounterID}-icon.jpg"

def extractSimplifiedFight(simplifiedFights:dict) -> Tuple[int, str]:
  """Return the encounterID and simplified fight data as a tuple."""
  return (list(simplifiedFights.items())[0])

def generateBestPullString(fight: dict) -> str:
  """Generates string to describe the best pull of a fight."""
  bestPull, fightTier = fight["bestPull"], fight["fightTier"]
  startTime, endTime = bestPull["startTime"],  bestPull["endTime"]
  timeElapsed = math.floor((endTime - startTime) / 1000)
  minutes, seconds = timeElapsed//60, timeElapsed%60
  if bestPull["kill"]:
    return f"Clear in {minutes}:{seconds}"
  else:
    if fight["fightTier"] == 3:
      return f'Phase {bestPull["lastPhase"]} - {bestPull["bossPercentage"]}% remaining'
    else:
      return f'{bestPull["fightPercentage"]}% remaining'

def generateSingleFightEmbed():
  """Generate Embed for a report featuring a specific fight."""
  print("single fight")

def generateMultiFightEmbed(simplifiedFights: dict, dateStart: str, link: str, rankings: dict) -> Embed:
  """Generate Embed for a report featuring multiple fights of the same encounter."""
  print(rankings)
  encounterID, fight = extractSimplifiedFight(simplifiedFights)
  linkObject = urlparse(link)
  fightURLPrefix = f"{linkObject.scheme}://{linkObject.netloc + linkObject.path}"
  print(encounterID, fight)
  multiFightEmbed = Embed(title=f'{fight["name"]} - <t:{dateStart}:D>')
  multiFightEmbed.set_thumbnail(url=generateImageURL(encounterID))
  multiFightEmbed.add_field(name="Pulls", value=fight["pullCount"], inline=False)
  clearPulls = ""
  if not fight["clearPulls"]: 
    clearPulls += "❌"
  else:
    for fightID in fight["clearPulls"]:
      clearPulls += f"[{generateClearEmoji(fightID, rankings)}]({fightURLPrefix}#fight={fightID}) "
  multiFightEmbed.add_field(name="Clear Pulls?", value=clearPulls, inline=False)
  bestPullString = generateBestPullString(fight)
  bestPullID = fight["bestPull"]["id"]
  # TODO: CHANGE BEST PULL TO FASTEST PARSE
  multiFightEmbed.add_field(name="Best Pull", 
                            value=f'[{bestPullString}]({fightURLPrefix}#fight={bestPullID})',
                            inline=False)

  multiFightEmbed.add_field(name="Best Parse", value="[Ybolgblaet Lammstymm - On track to a 100 on Machinist](https://www.google.com)",
                            inline=False)
  # TODO: ADD BEST PARSE FIELD WITH LINK TO FIGHT WITH THAT PARSE

  # generateEmbedColor(fight["bestPull"], rankings)
  multiFightEmbed.color = generateEmbedColor(fight["bestPull"], rankings)
  return multiFightEmbed

def generateCompilationEmbed():
  """Generate Embed for a report featuring multiple encounters."""
  print("multiple encounters")

def generateEmbedFromReport(reportData: dict, link: str, description: str = "") -> Embed:
  """
  Generates a Discord Embed from report data acquired from an FFLogs query.
  
  Args:
    `reportData`: A dict representing a json object containing reportData.

  Returns:
    A Discord Embed featuring relevant infomation such as the name of the fight,
    date, number of pulls, whether the fight was cleared, etc.
  
  Raises:
    `ReportDataError`: the reportData is not correctly formatted or missing.
  """
  # print(reportData)
  if "errors" in reportData:
     raise ReportDataError("The received report data is not correctly formatted or missing.")
  # print(reportData.get("data").get("reportData"))
  actors, dateStart, fights, rankings = extractReportFields(reportData)

  #The keys to both dicts are numbers.
  simplifiedRankings = dict(map(simplifyRanking, rankings))
  simplifiedActors = dict(map(simplifyActor, actors))
  simplifiedFights = reduceFights(fights, simplifiedRankings)

  print(simplifiedFights)
  returnEmbed = None

  if len(simplifiedFights) == 1:
    returnEmbed = generateMultiFightEmbed(simplifiedFights, dateStart, link, simplifiedRankings)
  else:
    returnEmbed = generateCompilationEmbed()
  # print(simplifiedActors)
  returnEmbed.url = link
  returnEmbed.description = description
  return returnEmbed

if __name__ == "__main__":
  dir = os.path.dirname(__file__)
  mockUltReport, mockExtremeReport, mockCompilationReport = None, None, None
  with open(os.path.join(dir, "test_data/ultimate.json"), "r") as f:
    mockUltReport = json.load(f)
  with open(os.path.join(dir, "test_data/extreme.json"), "r") as f:
    mockExtremeReport = json.load(f)
  with open(os.path.join(dir, "test_data/compilation.json"), "r") as f:
     mockCompilationReport = json.load(f)
  print(generateEmbedFromReport(mockExtremeReport, "lol").to_dict())
  generateEmbedFromReport(mockUltReport, "nope")
  generateEmbedFromReport(mockCompilationReport, "big boy")