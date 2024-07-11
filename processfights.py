from collections import namedtuple
from enum import Enum

EncounterSummary = namedtuple("EncounterSummary",
                              ["name", "pullCount", "clearPulls", 
                               "bestPull", "fightTier", "bestRanking"])
Ranking = namedtuple("Ranking", ["character", "parse", "job"])
Difficulty = Enum("Difficulty", ["UNRANKED", "EXTREME", "SAVAGE", "ULTIMATE"])


class ReportDataError(Exception):
  """The received reportData is not correctly formatted or missing."""

def getBestRanking(fightID: int) -> Ranking:
  pass

def processFights(reportData: dict) -> dict:
  """Returns a dict of fights, mapping fightIDs to fight data."""
  if "errors" in reportData:
    raise ReportDataError("The received report data is not correctly formatted or missing.")