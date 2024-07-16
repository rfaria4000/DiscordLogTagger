from discord import Embed
from typing import Tuple, List, NamedTuple
from collections import namedtuple
from enum import IntEnum
from urllib.parse import urlparse

import processfights as pf
import json, os, math, re

class PullState(IntEnum):
  WIPE = 0
  KILL = 1
  GRAY = 2
  GREEN = 3
  BLUE = 4
  PURPLE = 5
  ORANGE = 6
  PINK = 7
  GOLD = 8

#TODO: Make a config file that will pull custom emojis for the bot

WIPE_HEXCODE = 0xff0000
UNRANKED_CLEAR_HEXCODE = 0xabebc6
PARSE_HEXCODES = [0x666666, 0x1eff00, 0x0070ff, 0xa335ee, 0xff8000, 0xe268a8, 0xe5cc80]

NO_CLEARS_EMOJI = "❌"
UNRANKED_CLEAR_EMOJI = "✅"
PARSE_EMOJIS = ["🩶", "💚", "💙", "💜", "🧡", "🩷", "💛"]

Ranking = namedtuple("Ranking", ["character", "parse", "job"])

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

def generateEmbed(reportData: dict, link:str, desc:str = "") -> Embed:
  parsedLink = urlparse(link)
  specificFight = None
  if parsedLink.fragment:
    try:
      specificFight = int(re.search("(?<=fight=).*(?=&)", parsedLink.fragment).group())
    except Exception:
      pass
  processedFight = pf.processFights(reportData, specificFight)

  # if specificFight: return generateSingleFightEmbed()
  # if len(processedFight.fightSummaries) == 1: return generateMultiFightEmbed()
  # return generateCompilationEmbed()

if __name__ == "__main__":
  testLinkUltNoFragment = """
    https://www.fflogs.com/reports/7Myb4A6dDq1HnWvc
  """
  dir = os.path.dirname(__file__)
  mockUltReport, mockExtremeReport, mockCompilationReport = None, None, None
  with open(os.path.join(dir, "test_data/ultimate.json"), "r") as f:
    mockUltReport = json.load(f)
  generateEmbed(mockUltReport, testLinkUltNoFragment)
  # with open(os.path.join(dir, "test_data/extreme.json"), "r") as f:
  #   mockExtremeReport = json.load(f)
  # with open(os.path.join(dir, "test_data/compilation.json"), "r") as f:
  #    mockCompilationReport = json.load(f)
  # print(generateEmbedFromReport(mockExtremeReport, "lol").to_dict())
  # generateEmbedFromReport(mockUltReport, "nope")
  # generateEmbedFromReport(mockCompilationReport, "big boy")