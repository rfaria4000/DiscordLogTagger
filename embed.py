from discord import Embed
from datetime import datetime

from typing import Tuple, List
import json, os


class ReportDataError(Exception):
    """The received reportData is not correctly formatted or missing."""

def isFightUltimate(fight: dict) -> bool:
   """Returns whether a fight is an Ultimate."""
   return fight.get("lastPhase") > 0

def isFightSavage(fight: dict) -> bool:
   """Returns whether a fight is a Savage."""
   return fight.get("difficulty") == 101

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

  startTimeUNIX = flattenedReport.get("startTime") // 1000 #millisecond precision
  startTimeString = datetime.fromtimestamp(startTimeUNIX).strftime("%B %d, %Y")

  fightsList = flattenedReport.get("fights")

  rankingsList = flattenedReport.get("rankings").get("data")

  return actorList, startTimeString, fightsList, rankingsList

def simplifyRanking(ranking: dict) -> tuple:
  """Convert a ranking object into a tuple with fightIDs and list of player parses."""
  characterParseList = []
  for role in ranking["roles"].values():
     for player in role["characters"]:
        # Tanks and healers have a combined player field - this prunes that 
        if "name_2" in player: continue
        characterParseList.append((player["name"], player["rankPercent"]))
  return (ranking.get("fightID"), characterParseList)
  
def simplifyActor(actor: dict) -> list:
   """Convert a dict representing an actor to a list of id and name."""
   return actor.values()

def reduceFights(fights: dict, simplifiedRankings: dict):
  """Converts list of fight objects into a dict of unique fights with aggregate data."""
  fightDict = {}
  bestPull = None
  for fight in fights:
    encounterID = fight["encounterID"]
    if not encounterID in fightDict.keys():
      fightDict[encounterID] = {
         "name": fight["name"],
         "pulls": 0,
         "clearPulls": [],
         "bestPullID": fight["id"]
      }
      bestPull = fight
    fightDict[encounterID]["pulls"] += 1
    if fight['kill']: fightDict[encounterID]["clearPulls"].append(fight["id"])
  print(fightDict)

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
  actors, dateString, fights, rankings = extractReportFields(reportData)
  fightsNameSet =set([fight.get("name") for fight in fights])
  # print(fights)
  titleFight = ""
  if len(fightsNameSet) == 1:
     titleFight = next(iter(fightsNameSet))
  else:
    titleFight = "Multiple Fights"
    description = "Fights: " + ", ".join([fightName for fightName in fightsNameSet])

  pullTotal = len(fights)

  #The keys to both dicts are numbers.
  simplifiedRankings = dict(map(simplifyRanking, rankings))
  simplifiedActors = dict(map(simplifyActor, actors))

  print(reduceFights(fights, simplifiedRankings))

  reportEmbed = Embed(title=titleFight + " - " + dateString)
  reportEmbed.description = description
  reportEmbed.add_field(name="Pulls", value=pullTotal, inline=False)
  reportEmbed.add_field(name="Clear?", value=True, inline=True)
  reportEmbed.url = link

  # print(dateString)

  return reportEmbed

if __name__ == "__main__":
  dir = os.path.dirname(__file__)
  mockUltReport, mockExtremeReport, mockCompilationReport = None, None, None
  with open(os.path.join(dir, "test_data/ultimate.json"), "r") as f:
    mockUltReport = json.load(f)
  with open(os.path.join(dir, "test_data/extreme.json"), "r") as f:
    mockExtremeReport = json.load(f)
  with open(os.path.join(dir, "test_data/compilation.json"), "r") as f:
     mockCompilationReport = json.load(f)
  generateEmbedFromReport(mockExtremeReport, "lol")
  generateEmbedFromReport(mockUltReport, "nope")
  generateEmbedFromReport(mockCompilationReport, "big boy")