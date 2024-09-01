from discord import Embed
from typing import Tuple, List, NamedTuple, Dict, Callable
from enum import IntEnum
from urllib.parse import urlparse, urlunparse, ParseResult
from functools import reduce

from datetime import datetime
from data.emoji import emojiDict
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

PULL_HEXCODES = [0xff0000, 0xabebc6, 0x666666, 0x1eff00, 0x0070ff, 
                 0xa335ee, 0xff8000, 0xe268a8, 0xe5cc80]
PULL_EMOJIS = ["❌", "✅", "🩶", "💚", "💙", "💜", "🧡", "🩷", "💛"]

FIELD_VALUE_LIMIT = 1024
FIELD_VALUE_TRUNCATE = 1021

class BestPullPreview(NamedTuple):
  description: str
  fightID: int

class SingleFightInfo(NamedTuple):
  playersString: str
  parseString: str

class NotableFightOverview(NamedTuple):
  name: str
  pulls: int
  clears: str

def isSingleFight(report:pf.ReportSummary) -> bool:
  return (len(report.fightSummaries) == 1
          and report.fightSummaries[0]["pullCount"] == 1)

def isCompilation(report:pf.ReportSummary) -> bool:
  return len(report.fightSummaries) > 1

def generateTitle(report: pf.ReportSummary) -> str:
  if isCompilation(report): return "💠 Multiple Fights"
  else: return (("🔸 " if isSingleFight(report) else "🔷 ") +
    report.fightSummaries[0]["name"])

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

#TODO: IF ENCOUNTERS SORTED, DON'T NEED HIGHLIGHT FIGHT ANYMORE, NO?
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

def bestPullSummary(encounter: dict) -> BestPullPreview:
  """Generates string to describe the best pull of a fight."""
  summary = ""
  highlightPull, fightTier = encounter["highlightPull"], encounter["fightTier"]
  startTime, endTime = highlightPull["startTime"],  highlightPull["endTime"]
  timeElapsed = math.floor((endTime - startTime) / 1000)
  minutes, seconds = timeElapsed//60, timeElapsed%60
  if highlightPull["kill"]:
    summary =  f"Clear in {minutes}:{seconds:02d}"
  else:
    if fightTier == pf.FightTier.ULTIMATE:
      summary = f'Phase {highlightPull["lastPhase"]} - {highlightPull["bossPercentage"]}% remaining'
    else:
      summary = f'{highlightPull["fightPercentage"]}% remaining'
  return BestPullPreview(summary, highlightPull["id"])

def generateClearEmojis(encounter: dict, 
                        addLink: Callable[[str, int], int]) -> str:
  clears = encounter["clearPulls"]
  if not clears: return PULL_EMOJIS[Pull.WIPE]
  
  emojiList = list(map(lambda pull: (PULL_EMOJIS[parseToIndex(pull.bestParse)], 
                                     pull.fightID), clears))
  return str(reduce(lambda x, y: x + (addLink(*y)), emojiList, ""))

def singleFightPlayersInfo(encounter: dict) -> SingleFightInfo:
  rankings = deepcopy(encounter["highlightPull"]["friendlyPlayers"])
  
  sortedPlayerRankings = sorted(rankings, key=lambda player: 
                                  emojiDict[player.job].priority
                               )
  playerEmojiMap = lambda ranking: (emojiDict[ranking.job].emoji + " "  
                                      + ranking.character)
  playerString = "\n".join(map(playerEmojiMap, sortedPlayerRankings))

  playerFilteredRankings = filter(lambda ranking: ranking.parse >= 0, 
                                  sortedPlayerRankings)
  if not playerFilteredRankings: return (playerString, "")
  parseEmojiMap = lambda ranking: str(emojiDict[ranking.job].emoji + " " +
                                      PULL_EMOJIS[parseToIndex(ranking.parse)] + 
                                      " " + str(ranking.parse))
  parseString = "\n".join(map(parseEmojiMap, playerFilteredRankings))

  return SingleFightInfo(playerString, parseString)

def filterEncounters(encounters: List[Dict]) -> List[Dict]:
  filterUnranked = lambda encounter: encounter["fightTier"] > pf.FightTier.UNRANKED
  filteredEncounters = list(filter(filterUnranked, encounters))
  if not filteredEncounters: filteredEncounters = encounters
  return filteredEncounters

# Used to populate the overview - add up fights in order until string limit
# for field reached? 
def compilationFightsToString(encounters: List[Dict]) -> str:
  encountersString = ", ".join(encounter["name"] for encounter in filterEncounters(encounters))
  if len(encountersString) > FIELD_VALUE_LIMIT: 
    return (encountersString[FIELD_VALUE_TRUNCATE:] + "...") 
  return encountersString

# Select up to max 5 fights to highlights 
# (order the list then pick out the top 5?)
#TODO: Hammer down the type for the list return - return tuple of 3 strings?
#name, pulls, clears?
def compilationHighlightFights(encounters: List[Dict], 
                               addLink: Callable[[str, int], int]) -> List[NotableFightOverview]:
  # grab the encounters, order them by compareFight? might have to do that in 
  # process fights
  notableEncounters = filterEncounters(encounters)
  fightOverviews = []
  for encounter in notableEncounters:
    fightOverviews.append(NotableFightOverview(encounter["name"], 
                                               str(encounter["pullCount"]), 
                                               generateClearEmojis(encounter, 
                                                                   addLink)))
  return fightOverviews

def generateFields(report:pf.ReportSummary, 
                   parsedLink:ParseResult) -> List[Dict[str, str]]:
  fields = []
  addLink = makeLinkGenerator(parsedLink)
  addField = makeFieldsAdder(fields)
  if isCompilation(report):
    addField("Fight Type", "Compilation", False)
    addField("Notable Fights", compilationFightsToString(report.fightSummaries), 
             False)
    for highlight in compilationHighlightFights(report.fightSummaries, addLink):
      addField(f"{highlight.name} - {highlight.pulls} pull(s)", 
               f"Clears: {highlight.clears}", False)
  else:
    bestPullInfo = bestPullSummary(report.fightSummaries[0])
    # print(bestPullInfo)
    if isSingleFight(report):
      playerInfo = singleFightPlayersInfo(report.fightSummaries[0])
      addField("Fight Type", "Single", False)
      addField("Status", bestPullInfo.description, False)
      addField("Party", playerInfo.playersString, True)
      if playerInfo[1]: addField("Parses", playerInfo.parseString, True)
    else:
      addField("Fight Type", "Multi", False)
      addField("Pulls", str(report.fightSummaries[0]["pullCount"]), False)
      addField("Best Pull", addLink(*bestPullInfo), False)
      addField("Clears?", generateClearEmojis(report.fightSummaries[0], addLink), False)
  return fields

def getChosenFight(linkObject: ParseResult) -> int:
  if linkObject.fragment:
    searchResults = re.search(r"(?<=fight=).*", linkObject.fragment)
    if searchResults:
      searchResults = searchResults.group(0).split("&")[0]
      if searchResults == "last": return -1
      if searchResults.isnumeric(): return int(searchResults)
  return 0

def generateEmbed(reportData: dict, link:str, desc:str = "") -> Embed:
  parsedLink = urlparse(link.replace("\n", "").strip())
  print(getChosenFight(parsedLink))
  processedFight = pf.processFights(reportData, getChosenFight(parsedLink))
  print(processedFight)

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
  with open(os.path.join(dir, "tests/test_data/ultimate.json"), "r") as f:
    mockUltReport = json.load(f)
  with open(os.path.join(dir, "tests/test_data/compilation.json"), "r") as f:
    mockCompilationReport = json.load(f)
  generateEmbed(mockUltReport, testLinkUltNoFragment)  
  generateEmbed(mockCompilationReport, testCompliationLink)
  # link = "https://www.fflogs.com/reports/gnNm23A8DHp9Kch7#fight=last&type=damage-done"
  # testLinkObject = urlparse(link.replace("\n", "").strip())
  # print(getChosenFight(testLinkObject))

  # with open(os.path.join(dir, "test_data/extreme.json"), "r") as f:
  #   mockExtremeReport = json.load(f)
  # with open(os.path.join(dir, "test_data/compilation.json"), "r") as f:
  #    mockCompilationReport = json.load(f)
  # print(generateEmbedFromReport(mockExtremeReport, "lol").to_dict())
  # generateEmbedFromReport(mockUltReport, "nope")
  # generateEmbedFromReport(mockCompilationReport, "big boy")