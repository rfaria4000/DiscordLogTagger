from typing import Callable, Tuple

from collections import namedtuple
from enum import Enum

EncounterSummary = namedtuple("EncounterSummary",
                              ["name", "pullCount", "clearPulls", 
                               "bestPull", "fightTier", "bestRanking"])
RankingSummary = namedtuple("RankingSummary", ["character", "parse", "job"])
ReportFields = namedtuple("ReportFields", ["owner", "actors", "startTime",
                                           "fights", "rankings"])
ReportSummary = namedtuple("ReportSummary", ["owner", "startTime", "fightSummaries"])
FightTier = Enum("FightTier", ["UNRANKED", "EXTREME", "SAVAGE", "ULTIMATE"])

class ReportDataError(Exception):
  """The received reportData is not correctly formatted or missing."""

def makeTierEvaluator(rankings: dict) -> Callable[[dict], int]:
  """Return a function that returns the tier of a fight."""
  def evaluateDifficulty(fight: dict) -> int:
    if fight["lastPhase"] > 0: return FightTier.ULTIMATE
    if fight["difficulty"] == 101: return FightTier.SAVAGE
    if fight["id"] in rankings.keys(): return FightTier.EXTREME
    return FightTier.UNRANKED
  
  return evaluateDifficulty

def bestRanking(fightID: int) -> RankingSummary:
  pass

def processFights(reportData: dict) -> dict:
  """Returns a dict of fights, mapping fightIDs to fight data."""
  if "errors" in reportData:
    raise ReportDataError("The received report data is not correctly formatted or missing.")
  
  return ReportSummary()
  
if __name__ == "__main__":
  #TODO: bring over testing function from embed
  pass