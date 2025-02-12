import discord
from typing import Optional
from encounter import Encounter
from fight import Fight

class Report:
  """
  Represents a combat report on FFLogs.
  """
  def __init__(self, reportData: dict[str, dict]):
    self.reportData = reportData
    self.encounterDict: dict[Encounter] = {}
    self.unpackData()
    self.sortFights()

  def unpackData(self):
    report: dict[str, dict] = self.reportData["data"]["reportData"]["report"]
    self.code: str = report["code"]
    self.author: str = report["owner"]["name"]
    self.actorData: list[dict] = report["masterData"]["actors"]
    self.fightData: list[dict] = report["fights"]
    # If there are no rankings, fflogs returns an empty list for ranking data
    self.rankingData: list[Optional[dict]] = report["rankings"]["data"]
    self.startTime: int = report["startTime"] // 1000 #millisecond precision
    self.url: str = f"https://www.fflogs.com/reports/{self.code}"

  def sortFights(self):
    for pull in self.fightData:
      pullEncounterID: int = pull["encounterID"]
      if pullEncounterID not in self.encounterDict.keys():
        self.encounterDict[pullEncounterID] = Encounter(pullEncounterID)
      
      pullRankings = next((x for x in self.rankingData 
                                if x["fightID"] == pull["id"]), None)
      fightObject = Fight(pull, self.actorData, pullRankings)
      self.encounterDict[pullEncounterID].addFight(fightObject)

  def addReportDataToEmbed(self, embed: discord.Embed) -> discord.Embed:
    embed.set_author(name=f"Uploaded by {self.author}")
    embed.title += f" - <t:{self.startTime}:D>"
    # TODO: modify once filter function is in place
    embed.url = self.url
    return embed

  def toEmbed(self, 
              link: str = None, 
              description: str = None) -> discord.Embed:
    returnEmbed = None
    # TODO: Add link validation
    if len(self.encounterDict) == 1:
      soleEncounter: Encounter = next(iter(self.encounterDict.values()), 
                                      Encounter())
      # TODO: include filter here for specified fight
      returnEmbed = soleEncounter.toEmbed(link = self.url, 
                                          description = description)
    else:
      returnEmbed = discord.Embed()
      returnEmbed.title = "💠 Multiple Fights"

    return self.addReportDataToEmbed(returnEmbed)

if __name__ == "__main__":
  import json, os

  dir = os.path.dirname(__file__)
  mockReportData = None
  with open(os.path.join(dir, "tests/test_data/compilation.json"), "r") as f:
    mockReportData = json.load(f)
  testReport = Report(mockReportData)
  testReport.sortFights()
  for k, v in testReport.encounterDict.items():
    print(f"Key: {k}\n{v.toEmbed().to_dict()}")