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

def makeTierEvaluator(rankings: dict) -> Callable[[dict], int]:
  """Return a function that returns the tier of a fight."""
  def evaluateDifficulty(fight: dict) -> int:
    if fight["lastPhase"] > 0: return FightTier.ULTIMATE
    if fight["difficulty"] == 101: return FightTier.SAVAGE
    if fight["id"] in rankings.keys(): return FightTier.EXTREME
    return FightTier.UNRANKED
  
  return evaluateDifficulty

def bestRanking(fightID: int) -> ReportSummary:
  pass

def processFights(reportData: dict) -> dict:
  """Returns a dict of fights, mapping fightIDs to fight data."""
  if "errors" in reportData:
    raise ReportDataError("The received report data is not correctly formatted or missing.")
  
  return ReportSummary()
  
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
  print(processFights(mockUltReport))