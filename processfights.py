from typing import Callable, Tuple, NamedTuple, Dict, List
from enum import Enum

import os, json

class ReportFields(NamedTuple):
  owner: str
  actors: list
  startTime: int
  fights: List[dict]
  rankings: List[dict]

class RankingSummary(NamedTuple): 
  character: str
  parse: int
  job: str

class EncounterSummary(NamedTuple):
  name: str
  pullCount: int
  clearPulls: list
  bestPull: dict #fights from report data
  fightTier: int
  bestRanking: RankingSummary

class ReportSummary(NamedTuple):
  owner: str
  startTime: int
  fightSummaries: Dict[int, EncounterSummary]

class FightTier(Enum):
  UNRANKED = 0
  EXTREME = 1
  SAVAGE = 2
  ULTIMATE = 3

# Aim: report Data -> ReportFields ->Dict[fightID, EncounterSummary]->ReportSummary
#                                 \->       RankingSummary        -/
class ReportDataError(Exception):
  """The received reportData is not correctly formatted or missing."""

def makeTierEvaluator(rankingSummaryDict: Dict[int, RankingSummary]) -> Callable[[dict], int]:
  """Return a function that returns the tier of a fight."""
  def evaluateDifficulty(fight: dict) -> int:
    if fight["lastPhase"] > 0: return FightTier.ULTIMATE
    if fight["difficulty"] == 101: return FightTier.SAVAGE
    if fight["id"] in rankingSummaryDict.keys(): return FightTier.EXTREME
    return FightTier.UNRANKED
  
  return evaluateDifficulty

def bestRanking(fightID: int) -> ReportSummary:
  pass

def generateFightRankingTuples(ranking: dict) -> Tuple[int, RankingSummary]:
  """Convert a ranking object into a tuple with fightIDs and list of player parses."""
  rankingSummaryList = []
  for role in ranking["roles"].values():
     for player in role["characters"]:
        # Tanks and healers have a combined player field - this prunes that 
        if "name_2" in player: continue
        rankingSummaryList.append(RankingSummary(player["name"], 
                                                 player["rankPercent"], 
                                                 player["class"]))
  return (ranking.get("fightID"), rankingSummaryList)

def extractReportFields(reportData: dict) -> Tuple[str, List[object], int, List[object], List[object]]:
  """
  Extracts the list of actors, date, and list of fights from a report.
   
   Args:
    `reportData`: A dict representing a json object containing reportData.

  Returns:
    A tuple containing the list of actor objects, the date of the report in 
    "Month Day, Year" format, a list of fights, and a possibly empty list of 
    rankings.
  """
  flattenedReport = reportData["data"]["reportData"]["report"]
  owner = flattenedReport["owner"]["name"]
  actorList = flattenedReport["masterData"]["actors"]
  startTime = flattenedReport["startTime"]  // 1000 # millisecond precision
  fightsList = flattenedReport["fights"]
  rankingsList = flattenedReport["rankings"]["data"]

  return ReportFields(owner, actorList, startTime, fightsList, rankingsList)

def processFights(reportData: dict) -> dict:
  """Returns a dict of fights, mapping fightIDs to fight data."""
  if "errors" in reportData:
    raise ReportDataError("The received report data is not correctly formatted or missing.")
  
  report = extractReportFields(reportData)
  # print(report.rankings)
  fightRankings = dict(map(generateFightRankingTuples, report.rankings))
  print(fightRankings)
  return ReportSummary(report.owner, report.startTime)
  
if __name__ == "__main__":
  #TODO: bring over testing function from embed
  dir = os.path.dirname(__file__)
  mockUltReport, mockExtremeReport, mockCompilationReport = None, None, None
  with open(os.path.join(dir, "test_data/ultimate.json"), "r") as f:
    mockUltReport = json.load(f)
  with open(os.path.join(dir, "test_data/extreme.json"), "r") as f:
    mockExtremeReport = json.load(f)
  with open(os.path.join(dir, "test_data/compilation.json"), "r") as f:
     mockCompilationReport = json.load(f)
  print(processFights(mockExtremeReport))