import discord
from typing import Optional
from encounter import Encounter
from fight import Fight, FightTier

NOTABLE_FIGHT_LIMIT = 5
URL_FIGHT_QUERY = "?fight={}"

class Report:
  """
  Represents a combat report on FFLogs.
  """
  def __init__(self, reportData: dict[str, dict]):
    self.reportData = reportData
    self.encounterDict: dict[Encounter] = {}
    self._unpackData()

  def _unpackData(self):
    report: dict[str, dict] = self.reportData["data"]["reportData"]["report"]
    self.code: str = report["code"]
    self.author: str = report["owner"]["name"]
    self.actorData: list[dict] = report["masterData"]["actors"]
    self.fightData: list[dict] = report["fights"]
    # If there are no rankings, fflogs returns an empty list for ranking data
    self.rankingData: list[Optional[dict]] = report["rankings"]["data"]
    self.startTime: int = report["startTime"] // 1000 #millisecond precision
    self.url: str = f"https://www.fflogs.com/reports/{self.code}"

  def _sortFights(self) -> None:
    for pull in self.fightData:
      pullEncounterID: int = pull["encounterID"]
      if pullEncounterID not in self.encounterDict.keys():
        self.encounterDict[pullEncounterID] = Encounter(pullEncounterID)
      
      pullRankings = next((x for x in self.rankingData 
                                if x["fightID"] == pull["id"]), None)
      fightObject = Fight(pull, self.actorData, pullRankings)
      self.encounterDict[pullEncounterID].addFight(fightObject)

  @property
  def notableEncounters(self) -> Optional[list[Encounter]]:
    if not self.encounterDict: return None

    sortedEncounters = sorted(self.encounterDict.values(), reverse = True)
    filterUnranked = lambda x: x.encounterTier > FightTier.UNRANKED
    filteredEncounters = list(filter(filterUnranked, sortedEncounters))
    if not filteredEncounters: filteredEncounters = sortedEncounters
    
    return filteredEncounters[:NOTABLE_FIGHT_LIMIT]

  @property
  def notableEncounterNames(self) -> Optional[str]:
    if not self.encounterDict: return None

    return ", ".join(map(lambda x: x.name, self.notableEncounters))

  def addReportDataToEmbed(self, 
                           embed: discord.Embed,
                           fightID: int = None) -> discord.Embed:
    embed.set_author(name=f"Uploaded by {self.author}")
    embed.title += f" - <t:{self.startTime}:D>"
    embed.url = self.url
    if fightID is not None:
      embed.url += URL_FIGHT_QUERY.format("last" if fightID == -1 else fightID)
    return embed

  def grabFightEmbedByID(self, 
                         fightID: int,
                         description: str = None) -> discord.Embed:
    if fightID == -1:
      fightID = self.fightData[-1]["id"]
    pullData = next((x for x in self.fightData 
                               if x["id"] == fightID), None)
    pullRankings = next((x for x in self.rankingData 
                                 if x["fightID"] == fightID), None)
    fightObject = Fight(pullData, self.actorData, pullRankings)
    return self.addReportDataToEmbed(fightObject.toEmbed(description), fightID)

  def toEmbed(self, 
              link: str = None, 
              description: str = None) -> discord.Embed:
    self._sortFights()

    if len(self.encounterDict) == 1:
      soleEncounter: Encounter = next(iter(self.encounterDict.values()), 
                                      Encounter())
      return self.addReportDataToEmbed(soleEncounter.toEmbed(self.url, 
                                                             description))
    

    highlightEncounter = self.notableEncounters[0]
    reportEmbed = discord.Embed()
    reportEmbed.title = "💠 Multiple Fights"
    reportEmbed.color = highlightEncounter.bestFight.color
    reportEmbed.set_thumbnail(url = highlightEncounter.bestFight.thumbnailURL)
    
    reportEmbed.add_field(name = "Notable Fights",
                          value = self.notableEncounterNames,
                          inline = False)

    for enc in self.notableEncounters:
      reportEmbed.add_field(name = f"{enc.name} - {enc.pulls} pull(s)",
                            value = f"Clears: {enc.clearPullsEmojis(self.url)}",
                            inline = False)

    return self.addReportDataToEmbed(reportEmbed)

if __name__ == "__main__":
  import json, os

  dir = os.path.dirname(__file__)
  mockReportData = None
  with open(os.path.join(dir, "tests/test_data/compilation.json"), "r") as f:
    mockReportData = json.load(f)
  testReport = Report(mockReportData)
  testReport._sortFights()
  # print(encounter.name for encounter in testReport.notableEncounters)
  for encounter in testReport.notableEncounters:
    print(encounter.name)
  # for k, v in testReport.encounterDict.items():
  #   print(f"Key: {k}\n{v.toEmbed().to_dict()}")