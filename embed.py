from discord import Embed
from typing import Tuple, List, NamedTuple, Dict, Callable
from collections import namedtuple
from enum import IntEnum
from urllib.parse import urlparse, urlunparse, ParseResult
from functools import reduce

from datetime import datetime
from emoji import emojiDict
from copy import deepcopy
import processfights as pf
import json, os, math, re

class Pull(IntEnum):
  WIPE = 0
  CLEAR = 1
  GRAY = 2
  GREEN = 3
  BLUE = 4
  PURPLE = 5
  ORANGE = 6
  PINK = 7
  GOLD = 8

#TODO: Make a config file that will pull custom emojis for the bot
PULL_HEXCODES = [0xff0000, 0xabebc6, 0x666666, 0x1eff00, 0x0070ff, 
                 0xa335ee, 0xff8000, 0xe268a8, 0xe5cc80]
PULL_EMOJIS = ["❌", "✅", "🩶", "💚", "💙", "💜", "🧡", "🩷", "💛"]

# Ranking = namedtuple("Ranking", ["character", "parse", "job"])

def generateClearEmoji(fightID: dict, rankings:dict) -> str:
  """Generate an emoji based on a cleared fights."""
  if not fightID in rankings: return UNRANKED_CLEAR_EMOJI

  bestParse = 0
  for ranking in rankings[fightID]:
    bestParse = max(bestParse, ranking.parse) 

  return PARSE_EMOJIS[generateRankingColorIndex(bestParse)]

def extractSimplifiedFight(simplifiedFights:dict) -> Tuple[int, str]:
  """Return the encounterID and simplified fight data as a tuple."""
  return (list(simplifiedFights.items())[0])

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

  multiFightEmbed.add_field(name="Best Pull", value="[Ybolgblaet Lammstymm - On track to a 100 on Machinist](https://www.google.com)",
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

def isSingleFight(report:pf.ReportSummary) -> bool:
  return (len(report.fightSummaries) == 1
          and report.fightSummaries[0]["pullCount"] == 1)

def isCompilation(report:pf.ReportSummary) -> bool:
  return len(report.fightSummaries) > 1

def generateTitle(report: pf.ReportSummary) -> str:
  if isCompilation(report): return "Multiple Fights"
  else: return report.fightSummaries[0]["name"]

def generateImageURL(report: dict) -> str:
  """Generate a URL to a thumbnail based on the fight."""
  encounterID = 0
  if not isCompilation(report):
    encounterID = report.fightSummaries[0]["highlightPull"]["encounterID"]
  elif report.highlightEncounter["highlightPull"]["difficulty"] >= 100:
      encounterID = report.highlightEncounter["highlightPull"]["encounterID"]
  
  return f"https://assets.rpglogs.com/img/ff/bosses/{encounterID}-icon.jpg"

def parseToIndex(parse: int) -> int:
  """Return an index 0-6 for a list of possible outputs based on a parse."""
  # Ranges can be found here: 
  # https://www.archon.gg/ffxiv/articles/help/rankings-and-parses
  if parse == -1: return Pull.CLEAR
  elif parse < 25: return Pull.GRAY
  elif parse < 50: return Pull.GREEN
  elif parse < 75: return Pull.BLUE
  elif parse < 95: return Pull.PURPLE
  elif parse < 99: return Pull.ORANGE
  elif parse == 99: return Pull.PINK
  else: return Pull.GOLD

def compareClearParses(clearOne: pf.ClearPull, 
                       clearTwo: pf.ClearPull) -> pf.ClearPull:
  return clearOne if clearOne.bestParse > clearTwo.bestParse else clearTwo

def generateEmbedColor(report:pf.ReportSummary) -> int:
  """Generate a hex code for an Embed based on a fight."""
  highlightEncounter = report.highlightEncounter
  if len(highlightEncounter["clearPulls"]) == 0: return PULL_HEXCODES[Pull.WIPE]
  
  bestClear = reduce(compareClearParses, highlightEncounter["clearPulls"])
  return PULL_HEXCODES[parseToIndex(bestClear.bestParse)]

def makeFieldsAdder(fields: List[Dict[str, str]]) -> Callable[[str, str, bool], None]:
  def addField(name: str, value: str, inline:bool = False) -> None:
    fields.append(
      {
        "name": name,
        "value": value,
        "inline": inline
      }
    )
  
  return addField

def makeLinkGenerator(parsedLink: ParseResult) -> Callable[[str, int], str]:
  def addLinkToFight(text: str, fightId: int) -> str:
    """Turn text into a Markdown link to a specific fight."""
    fflogsPrefix = f"{parsedLink.scheme}://{parsedLink.netloc}{parsedLink.path}"
    return f"[{text}]({fflogsPrefix}/#fight={fightId})"

  return addLinkToFight

def bestPullSummary(encounter: dict) -> Tuple[str, int]:
  """Generates string to describe the best pull of a fight."""
  summary = ""
  highlightPull, fightTier = encounter["highlightPull"], encounter["fightTier"]
  startTime, endTime = highlightPull["startTime"],  highlightPull["endTime"]
  timeElapsed = math.floor((endTime - startTime) / 1000)
  minutes, seconds = timeElapsed//60, timeElapsed%60
  if highlightPull["kill"]:
    summary =  f"Clear in {minutes}:{seconds}"
  else:
    if fightTier == pf.FightTier.ULTIMATE:
      summary = f'Phase {highlightPull["lastPhase"]} - {highlightPull["bossPercentage"]}% remaining'
    else:
      summary = f'{highlightPull["fightPercentage"]}% remaining'
  return (summary, highlightPull["id"])

def generateClearEmojis(encounter: dict, 
                        addLink: Callable[[str, int], int]) -> str:
  clears = encounter["clearPulls"]
  if not clears: return PULL_EMOJIS[Pull.WIPE]
  
  emojiList = list(map(lambda pull: (PULL_EMOJIS[parseToIndex(pull.bestParse)], 
                                     pull.fightID), clears))
  return str(reduce(lambda x, y: x + (addLink(*y)), emojiList, ""))

def singleFightPlayerInfo(encounter: dict) -> Tuple[str, str]:
  rankings = deepcopy(encounter["highlightPull"]["friendlyPlayers"])
  
  sortedPlayerRankings = sorted(rankings, 
                                key=lambda player: emojiDict[player.job][1])
  playerEmojiMap = lambda ranking: emojiDict[ranking.job][0] + ranking.character
  playerString = "\n".join(map(playerEmojiMap, sortedPlayerRankings))

  playerFilteredRankings = filter(lambda ranking: ranking.parse >= 0, 
                                  sortedPlayerRankings)
  if not playerFilteredRankings: return (playerString, "")
  parseEmojiMap = lambda ranking: str(emojiDict[ranking.job][0] + 
                                      PULL_EMOJIS[parseToIndex(ranking.parse)] + 
                                      " " + str(ranking.parse))
  parseString = "\n".join(map(parseEmojiMap, playerFilteredRankings))

  return(playerString, parseString)

def generateFields(report:pf.ReportSummary, 
                   parsedLink:ParseResult) -> List[Dict[str, str]]:
  fields = []
  addLink = makeLinkGenerator(parsedLink)
  addField = makeFieldsAdder(fields)
  # print(report)
  if isCompilation(report):
    addField("Fight Type", "Compilation", False)
  else:
    bestPullInfo = bestPullSummary(report.fightSummaries[0])
    # print(bestPullInfo)
    if isSingleFight(report):
      playerInfo = singleFightPlayerInfo(report.fightSummaries[0])
      addField("Fight Type", "Single", False)
      addField("Status", bestPullInfo[0], False)
      addField("Party", playerInfo[0], True)
      if playerInfo[1]: addField("Parses", playerInfo[1], True)
    else:
      addField("Fight Type", "Multi", False)
      addField("Best Pull", addLink(*bestPullInfo), True)
      addField("Clears?", generateClearEmojis(report.fightSummaries[0], addLink), False)
  return fields

def generateEmbed(reportData: dict, link:str, desc:str = "") -> Embed:
  parsedLink = urlparse(link.replace("\n", "").strip())
  specificFight = None
  if parsedLink.fragment:
    specificFight = re.search(r"(?<=fight=)\d*", parsedLink.fragment)
    if specificFight: specificFight = int(specificFight.group(0))
  processedFight = pf.processFights(reportData, specificFight)
  print(parsedLink)

  reportEmbed = {
    "title": f"{generateTitle(processedFight)} - <t:{processedFight.startTime}:D>",
    "url": urlunparse(parsedLink),
    "description": desc,
    "author": {
      "name": f"Uploaded by {processedFight.owner}"
    },
    "thumbnail": {
      "url": generateImageURL(processedFight)
    },
    "color": generateEmbedColor(processedFight),
    "fields": generateFields(processedFight, parsedLink)
  }
  
  print(reportEmbed)
  return Embed.from_dict(reportEmbed)

if __name__ == "__main__":
  testLinkUltNoFragment = """
    https://www.fflogs.com/reports/7Myb4A6dDq1HnWvc#fight=3
  """
  testCompliationLink = """
    https://www.fflogs.com/reports/CRh38LcT7BzAdHyr
  """
  dir = os.path.dirname(__file__)
  mockUltReport, mockExtremeReport, mockCompilationReport = None, None, None
  with open(os.path.join(dir, "test_data/ultimate.json"), "r") as f:
    mockUltReport = json.load(f)
  with open(os.path.join(dir, "test_data/compilation.json"), "r") as f:
    mockCompilationReport = json.load(f)
  generateEmbed(mockUltReport, testLinkUltNoFragment)  
  generateEmbed(mockCompilationReport, testCompliationLink)

  # with open(os.path.join(dir, "test_data/extreme.json"), "r") as f:
  #   mockExtremeReport = json.load(f)
  # with open(os.path.join(dir, "test_data/compilation.json"), "r") as f:
  #    mockCompilationReport = json.load(f)
  # print(generateEmbedFromReport(mockExtremeReport, "lol").to_dict())
  # generateEmbedFromReport(mockUltReport, "nope")
  # generateEmbedFromReport(mockCompilationReport, "big boy")