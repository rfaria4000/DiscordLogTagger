from typing import Callable, Tuple, NamedTuple, Dict, List
from enum import Enum, IntEnum

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

class RankingFunctions(NamedTuple):
  difficulty: Callable[[dict], int]
  compareFights: Callable[[dict, dict], dict]
  bestParse: Callable[[int], int]

class ClearPull(NamedTuple):
  fightID: int
  bestParse: int

class ReportSummary(NamedTuple):
  owner: str
  startTime: int
  fightSummaries: Dict[int, dict]

class FightTier(IntEnum):
  UNRANKED = 0
  EXTREME = 1
  SAVAGE = 2
  ULTIMATE = 3

# Clear values for the purpose of comparing fights.
# Makes a clear of any fight with a rating higher than a pull off any fight.
CLEAR_RATING_BONUS = 3
CLEAR_THRESHOLD = 4

class PullState(Enum):
  WIPE = 0
  KILL = 1
  GRAY = 2
  GREEN = 3
  BLUE = 4
  PURPLE = 5
  ORANGE = 6
  PINK = 7
  GOLD = 8
# Aim: report Data -> ReportFields ->Dict[fightID, EncounterSummary]->ReportSummary
#                                 \->       RankingSummary        -/
class ReportDataError(Exception):
  """The received reportData is not correctly formatted or missing."""

def getFightDuration(fight: dict) -> int:
  return fight["endTime"] - fight["startTime"]

def makeRankingFunctions(fightRankings: Dict[int, RankingSummary]) -> RankingFunctions:
  """Return a function that returns the tier of a fight."""
  def evaluateDifficulty(fight: dict) -> int:
    if fight["lastPhase"] > 0: return FightTier.ULTIMATE
    if fight["difficulty"] == 101: return FightTier.SAVAGE
    if fight["id"] in fightRankings.keys(): return FightTier.EXTREME
    return FightTier.UNRANKED
  
  def bestRanking(fightID: int) -> int:
    """Return the best parse for a fight, or -1 if the fight has no rankings."""
    if not fightID in fightRankings.keys(): return -1
    return max(map(lambda ranking: ranking.parse, fightRankings[fightID]))

  def compareFights(fightOne: dict, fightTwo: dict) -> dict:
    """
    Return the more salient of the two fights.

    Priority is, in order: clear (if above tier 0), fight difficulty, fight duration.
    For right now, fights with different names in the same tier will prioritize longer fights.
    """

    fightOneRating = evaluateDifficulty(fightOne)
    fightTwoRating = evaluateDifficulty(fightTwo)

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
 
  return RankingFunctions(evaluateDifficulty, compareFights, bestRanking)

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

def generateEncounters(fights: dict, rankingFunctions: RankingFunctions) -> dict:
  """Converts list of fight objects into a dict of unique fights with aggregate data."""
  encounters = {}
  for fight in fights:
    encounterID = fight["encounterID"]

    if not encounterID in encounters.keys():
      encounters[encounterID] = {
         "name": fight["name"],
         "pullCount": 0,
         "clearPulls": [],
         "bestPull": fight,
         "fightTier": rankingFunctions.difficulty(fight)
      }

    fightEncounter = encounters[encounterID]
    fightEncounter["pullCount"] += 1
    
    if fight['kill']: 
      fightEncounter["clearPulls"].append(
        ClearPull(fight["id"], rankingFunctions.bestParse(fight["id"]))
      )
      fightEncounter["fightTier"] = rankingFunctions.difficulty(fight)
    
    fightEncounter["bestPull"] = rankingFunctions.compareFights(fight, fightEncounter["bestPull"])
  return encounters

def processFights(reportData: dict) -> dict:
  """Returns a dict of fights, mapping fightIDs to fight data."""
  if "errors" in reportData:
    raise ReportDataError("The received report data is not correctly formatted or missing.")
  
  report: ReportFields = extractReportFields(reportData)
  # print(report.rankings)
  fightRankings: Dict[int, RankingSummary] = dict(map(generateFightRankingTuples, report.rankings))
  hydratedFunctions = makeRankingFunctions(fightRankings)
  encounters = generateEncounters(report.fights, hydratedFunctions)
  print(encounters)
  #TODO: Hydrate actors for best pull

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