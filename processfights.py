from typing import Callable, Tuple, NamedTuple, Dict, List
from enum import IntEnum
from copy import deepcopy
from functools import reduce
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
  fightSummaries: list
  highlightEncounter: dict

class FightTier(IntEnum):
  UNRANKED = 0
  RANKED = 1 #Extremes and Normal Raids
  SAVAGE = 2
  ULTIMATE = 3

# Clear values for the purpose of comparing fights.
# Makes a clear of any fight with a rating higher than a pull off any fight.
CLEAR_RATING_BONUS = 3
CLEAR_THRESHOLD = 4

# Aim: report Data -> ReportFields ->Dict[fightID, EncounterSummary]->ReportSummary
#                                  \--------RankingSummary---------/
class ReportDataError(Exception):
  """The received reportData is not correctly formatted or missing."""

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

def makeRankingFunctions(fightRankings: Dict[int, RankingSummary]) -> RankingFunctions:
  """Return a function that returns the tier of a fight."""
  def evaluateDifficulty(fight: dict) -> int:
    if fight["lastPhase"] > 0: return FightTier.ULTIMATE
    if fight["difficulty"] == 101: return FightTier.SAVAGE
    if fight["id"] in fightRankings.keys(): return FightTier.RANKED
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
    def getFightDuration(fight: dict) -> int:
      return fight["endTime"] - fight["startTime"]
    
    fightOneRating = evaluateDifficulty(fightOne)
    fightTwoRating = evaluateDifficulty(fightTwo)

    if fightOneRating and fightOne["kill"]: fightOneRating += CLEAR_RATING_BONUS
    if fightTwoRating and fightTwo["kill"]: fightTwoRating += CLEAR_RATING_BONUS

    if fightOneRating != fightTwoRating: 
      return fightOne if fightOneRating > fightTwoRating else fightTwo
    
    if fightOneRating < CLEAR_THRESHOLD:
      return fightOne if fightOne["fightPercentage"] < fightTwo["fightPercentage"] else fightTwo

    if fightOne["difficulty"] > fightTwo["difficulty"]: return fightOne
    if fightTwo["difficulty"] > fightOne["difficulty"]: return fightTwo

    isFightOneShorter = getFightDuration(fightOne) < getFightDuration(fightTwo)

    if fightOne["name"] == fightTwo["name"]:
      return fightOne if isFightOneShorter else fightTwo
    else:
      return fightTwo if isFightOneShorter else fightOne
 
  return RankingFunctions(evaluateDifficulty, compareFights, bestRanking)

def generateEncounters(fights: dict, rankingFunctions: RankingFunctions) -> list:
  """Converts list of fight objects into a dict of unique fights with aggregate data."""
  encounters = {}
  for fight in fights:
    encounterID = fight["encounterID"]

    if not encounterID in encounters.keys():
      encounters[encounterID] = {
         "name": fight["name"],
         "pullCount": 0,
         "clearPulls": [],
         "highlightPull": fight,
         "fightTier": rankingFunctions.difficulty(fight)
      }

    fightEncounter = encounters[encounterID]
    fightEncounter["pullCount"] += 1
    
    if fight['kill']: 
      fightEncounter["clearPulls"].append(
        ClearPull(fight["id"], rankingFunctions.bestParse(fight["id"]))
      )
      fightEncounter["fightTier"] = rankingFunctions.difficulty(fight)
    
    fightEncounter["highlightPull"] = rankingFunctions.compareFights(fight, fightEncounter["highlightPull"])
  return list(encounters.values())

def populateActors(encounters: list, actors: Dict[int, str], rankings):
  encountersCopy = deepcopy(encounters)
  for index, encounter in enumerate(encountersCopy):
    highlightPull = encounter["highlightPull"]
    friendlyPlayers = highlightPull["friendlyPlayers"]
    
    if highlightPull["id"] in rankings.keys():
      encountersCopy[index]["highlightPull"]["friendlyPlayers"] = rankings[highlightPull["id"]]
    else:
      playerList = list(map((lambda actorID: RankingSummary(actors[actorID][0], -1, actors[actorID][1])), friendlyPlayers))
      filteredPlayers = list(filter(lambda player: player[2] != "LimitBreak", playerList))
      encountersCopy[index]["highlightPull"]["friendlyPlayers"] = filteredPlayers
  
  return encountersCopy

def processFights(reportData: dict, specifiedFight: int = None) -> ReportSummary:
  # TODO: Update docstrings for entire file
  """."""
  if "errors" in reportData:
    raise ReportDataError("The received report data is not correctly formatted or missing.")
  
  report: ReportFields = extractReportFields(reportData)
  actors = dict(map((lambda actor: (list(actor.values())[0], list(actor.values())[1:])), report.actors))
  fightRankings: Dict[int, RankingSummary] = dict(map(generateFightRankingTuples, report.rankings))
  hydratedFunctions = makeRankingFunctions(fightRankings)
  encounters = None
  
  if specifiedFight:
    fight = list(filter((lambda fight: fight["id"] == specifiedFight), report.fights))
    encounters = generateEncounters(fight, hydratedFunctions)
  else:
    encounters = generateEncounters(report.fights, hydratedFunctions)
  
  populatedEncounters = populateActors(encounters, actors, fightRankings)

  def compareEncounters(x, y):
    xHighlight, yHighlight = x["highlightPull"], y["highlightPull"]
    return x if hydratedFunctions.compareFights(xHighlight, yHighlight) == xHighlight else y
  highlightEncounter = reduce(compareEncounters, populatedEncounters)

  sortedEncounters = sorted(populatedEncounters, 
                            key=lambda encounter: encounter["fightTier"],
                            reverse=True)
  
  return ReportSummary(report.owner, report.startTime, sortedEncounters, highlightEncounter)
  
if __name__ == "__main__":
  dir = os.path.dirname(__file__)
  mockUltReport, mockExtremeReport, mockCompilationReport = None, None, None
  with open(os.path.join(dir, "test_data/ultimate.json"), "r") as f:
    mockUltReport = json.load(f)
  with open(os.path.join(dir, "test_data/extreme.json"), "r") as f:
    mockExtremeReport = json.load(f)
  with open(os.path.join(dir, "test_data/compilation.json"), "r") as f:
     mockCompilationReport = json.load(f)
  print(processFights(mockCompilationReport))