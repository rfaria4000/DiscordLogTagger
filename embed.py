from discord import Embed
from datetime import datetime

from typing import Tuple, List
import ast 

jsonString = """
{'data': {'reportData': {'report': {'masterData': {'actors': [{'id': -1, 'name': 'Environment'}, {'id': 1, 'name': 'Sol Li'}, {'id': 2, 'name': 'Twintania'}, {'id': 3, 'name': "Rai'en Enkidou"}, {'id': 4, 'name': 'Kara Kielle'}, {'id': 5, 'name': 'Violet Calistria'}, {'id': 6, 'name': 'Coconut Coco'}, {'id': 7, 'name': 'Vrag Szad'}, {'id': 8, 'name': 'Shadow Moons'}, {'id': 9, 'name': 'Atsume Alamort'}, {'id': 10, 'name': 'Multiple Players'}, {'id': 11, 'name': 'Carbuncle'}, {'id': 12, 'name': 'Garuda-Egi'}, {'id': 13, 'name': ''}, {'id': 14, 'name': 'Oviform'}, {'id': 15, 'name': 'Oviform'}, {'id': 16, 'name': 'Demi-Bahamut'}, {'id': 17, 'name': 'Ifrit-Egi'}, {'id': 18, 'name': 'Earthly Star'}, {'id': 19, 'name': 'Titan-Egi'}, {'id': 20, 'name': 'Nael Geminus'}, {'id': 21, 'name': 'Nael Deus Darnus'}, {'id': 22, 'name': 'Fang Of Light'}, {'id': 23, 'name': 'Tail Of Darkness'}, {'id': 24, 'name': 'Thunderwing'}, {'id': 25, 'name': 'Iceclaw'}, {'id': 26, 'name': 'Firehorn'}, {'id': 27, 'name': 'Limit Break'}, {'id': 28, 'name': 'Bahamut Prime'}, {'id': 29, 'name': 'Multiple Enemies'}, {'id': 30, 'name': 'Ragnar Thereux'}, {'id': 31, 'name': 'Yinyinji Yinji'}, {'id': 32, 'name': 'Juinta Reyon'}, {'id': 33, 'name': 'Peter Trash'}, {'id': 34, 'name': ''}, {'id': 35, 'name': 'Tato Chan'}, {'id': 36, 'name': ''}, {'id': 37, 'name': 'Keishypoo Uwu'}, {'id': 38, 'name': 'Farah Ragnall'}, {'id': 39, 'name': 'Ayleth Wright'}, {'id': 40, 'name': 'Pahja Amarah'}, {'id': 41, 'name': 'Ezrien Orais'}, {'id': 42, 'name': 'Cooked Toast'}, {'id': 43, 'name': 'Rory Grimms'}, {'id': 44, 'name': 'Venessa Skyborn'}, {'id': 45, 'name': 'Amybelle Teonis'}, {'id': 46, 'name': 'Asteon Vaerzel'}, {'id': 47, 'name': 'Sierra Fantasy'}, {'id': 48, 'name': "Xil'thas Gwathre'nun"}, {'id': 49, 'name': 'Toko Alouette'}, {'id': 50, 'name': 'Sylvan Thorne'}, {'id': 51, 'name': 'Mint Julep'}, {'id': 52, 'name': 'Ahri Kaedehara'}, {'id': 53, 'name': "Heaven's Night"}, {'id': 54, 'name': 'Liviana Noir'}, {'id': 55, 'name': 'Happy Peter'}, {'id': 56, 'name': 'Valeria Straylight'}, {'id': 57, 'name': 'Farah Ragnall'}, {'id': 58, 'name': 'Clive Yaeger'}, {'id': 59, 'name': 'Lady Akane'}, {'id': 60, 'name': 'Percy Ardenne'}, {'id': 61, 'name': 'Theophilain Majere'}, {'id': 62, 'name': 'Aura Doom'}, {'id': 63, 'name': 'Clotilde Valeroyant'}, {'id': 64, 'name': "Tae'yeon Kim"}, {'id': 65, 'name': 'Shoo Shoo'}, {'id': 66, 'name': 'Surya Sunbeam'}, {'id': 67, 'name': 'Ishtar Anastasia'}, {'id': 68, 'name': 'Zelolo Zelo'}, {'id': 69, 'name': 'Annette Hitachine'}, {'id': 70, 'name': 'Faye Veena'}, {'id': 71, 'name': 'Hikome Kabuto'}, {'id': 72, 'name': "Draug Ban'ul"}, {'id': 73, 'name': "Tae'yeon Kim"}, {'id': 74, 'name': 'Carbuncle'}, {'id': 75, 'name': 'Hikome Kabuto'}, {'id': 76, 'name': 'Carbuncle'}, {'id': 77, 'name': 'Thane Trychimar'}, {'id': 78, 'name': 'Jolene Nounet'}, {'id': 79, 'name': 'Earthly Star'}, {'id': 80, 'name': 'Dracuns Ryder'}, {'id': 81, 'name': 'Keishypoo Uwu'}, {'id': 82, 'name': 'Hikome Kabuto'}, {'id': 83, 'name': 'Marina Domek'}, {'id': 84, 'name': "D'cera Ress"}, {'id': 85, 'name': 'Gwynnalla Khaa'}, {'id': 86, 'name': 'Jing Coresh'}, {'id': 87, 'name': 'Veis Miret-njer'}, {'id': 88, 'name': 'Azie Emet'}, {'id': 89, 'name': 'Yuki Nonaka'}, {'id': 90, 'name': 'Shrathina Helaa'}, {'id': 91, 'name': "Amania Do'urden"}, {'id': 92, 'name': 'Ivyndra Wiltswys'}, {'id': 93, 'name': "Tae'yeon Kim"}, {'id': 94, 'name': 'Just Vibin'}, {'id': 95, 'name': 'Sar Tor'}, {'id': 96, 'name': 'Suju Kuan'}, {'id': 97, 'name': 'Vivi Hoshiko'}, {'id': 98, 'name': 'Frenchtoast Andsyrup'}, {'id': 99, 'name': 'Luxie Hart'}, {'id': 100, 'name': "Y' Y'"}, {'id': 101, 'name': 'Thar Stoksker'}, {'id': 102, 'name': 'Valryia Arwen'}, {'id': 103, 'name': 'Boltgir Ukrin'}, {'id': 104, 'name': 'Offucia Revale'}, {'id': 105, 'name': 'Alyaerys Chandler'}, {'id': 106, 'name': 'Sager Step-on-me'}, {'id': 107, 'name': 'Wodanaz Odr'}, {'id': 108, 'name': 'Rei Hayashi'}, {'id': 109, 'name': 'Nadaki Vanima'}, {'id': 110, 'name': 'Eos'}, {'id': 111, 'name': 'Kyoti Crestfallen'}, {'id': 112, 'name': "A'ster Tia"}, {'id': 113, 'name': 'Kakler Skinner'}, {'id': 114, 'name': 'Hikome Kabuto'}, {'id': 115, 'name': 'Atlanna Love'}, {'id': 116, 'name': 'Erma Tersanu'}, {'id': 117, 'name': 'Sojhin Pendrag'}, {'id': 118, 'name': 'Jensen Jakov'}, {'id': 119, 'name': 'Noai Dei-ijla'}, {'id': 120, 'name': 'Draco Blackfyre'}, {'id': 121, 'name': 'Yuki Nonaka'}, {'id': 122, 'name': 'Camellia Mercer'}, {'id': 123, 'name': 'Athena Whispersurge'}, {'id': 124, 'name': 'Frenchtoast Andsyrup'}, {'id': 125, 'name': 'Hikome Kabuto'}, {'id': 126, 'name': 'Snacky Cakes'}, {'id': 127, 'name': 'Stein Phite'}, {'id': 128, 'name': 'Weiss Von-drachenberg'}, {'id': 129, 'name': 'Stein Phite'}, {'id': 130, 'name': 'Farah Ragnall'}, {'id': 131, 'name': 'Bophades Ligmaseus'}, {'id': 132, 'name': 'Umeyasha Mellissan'}, {'id': 133, 'name': 'Rue Thaelmore'}, {'id': 134, 'name': 'Rokkr Raah-zen'}, {'id': 135, 'name': 'Oir Almathen'}, {'id': 136, 'name': 'Mochi Moks'}, {'id': 137, 'name': 'Fridge Dollar'}, {'id': 138, 'name': 'Farah Ragnall'}, {'id': 139, 'name': 'Erma Tersanu'}, {'id': 140, 'name': 'Ishtar Anastasia'}, {'id': 141, 'name': 'Lorian Cromwell'}, {'id': 142, 'name': 'Revy Ironcrusher'}, {'id': 143, 'name': 'Aqua Fair'}, {'id': 144, 'name': 'Entele Hyguar'}, {'id': 145, 'name': 'Ek Lethe'}, {'id': 146, 'name': 'Montreal Xur'}, {'id': 147, 'name': 'Tidane Locksquall'}, {'id': 148, 'name': 'Jyra Nimo'}, {'id': 149, 'name': 'Xaph Astraeus'}, {'id': 150, 'name': 'Yxel Yoshioka'}, {'id': 151, 'name': 'Zoey Raposa'}, {'id': 152, 'name': 'Kearan Shadowsong'}, {'id': 153, 'name': 'Vvee Ddee'}, {'id': 154, 'name': 'Salty Buttlet'}, {'id': 155, 'name': 'Mercy Mae'}, {'id': 156, 'name': 'Balado Dulado'}, {'id': 157, 'name': 'Alyxandria Hyromire'}, {'id': 158, 'name': 'Hikome Kabuto'}, {'id': 159, 'name': 'Mr Chedda'}, {'id': 160, 'name': 'Liv Twigsnapper'}, {'id': 161, 'name': 'Farah Ragnall'}, {'id': 162, 'name': 'Urvogel Teryx'}, {'id': 163, 'name': 'Yan Yans'}, {'id': 164, 'name': 'liturgic bell'}, {'id': 165, 'name': 'Hikome Kabuto'}, {'id': 166, 'name': 'Alyx Jay'}, {'id': 167, 'name': 'Hikome Kabuto'}, {'id': 168, 'name': 'Equidar Novasch'}, {'id': 169, 'name': 'Wodanaz Odr'}, {'id': 170, 'name': 'Aimi Nelas'}, {'id': 171, 'name': 'Amybelle Teonis'}, {'id': 172, 'name': 'Aimona Winter'}, {'id': 173, 'name': 'Nanet Moon'}, {'id': 174, 'name': 'Droknar Maverlis'}, {'id': 175, 'name': 'Shadow Hunt'}, {'id': 176, 'name': 'Raux Fort'}, {'id': 177, 'name': 'Rjomi Dei-ijla'}, {'id': 178, 'name': 'Ouka Ootori'}, {'id': 179, 'name': 'Evette Corvus'}, {'id': 180, 'name': 'Rev Ix'}, {'id': 181, 'name': 'Todd Finn'}, {'id': 182, 'name': 'Farah Ragnall'}, {'id': 183, 'name': 'Lucie Beaumont'}, {'id': 184, 'name': 'Yefkey Yekel'}, {'id': 185, 'name': "I'datih Tio"}, {'id': 186, 'name': 'Lucie Beaumont'}, {'id': 187, 'name': "I'datih Tio"}, {'id': 188, 'name': 'Berial Blackrose'}, {'id': 189, 'name': 'Arumy Shirai'}, {'id': 190, 'name': 'Luxie Hart'}, {'id': 191, 'name': ''}, {'id': 192, 'name': 'Asteon Vaerzel'}, {'id': 193, 'name': 'Droknar Maverlis'}, {'id': 194, 'name': 'Bibi Mbap'}, {'id': 195, 'name': 'Laerni Alina'}, {'id': 196, 'name': 'Laerni Alina'}, {'id': 197, 'name': 'Tori Rivers'}, {'id': 198, 'name': 'Vindur Surana'}, {'id': 199, 'name': 'Arika Chihoko'}, {'id': 200, 'name': 'Blue Hiei'}, {'id': 201, 'name': 'Blue Hiei'}, {'id': 202, 'name': 'Tsunderelf Xae'}, {'id': 203, 'name': 'Lilipo Lilimo'}, {'id': 204, 'name': 'Asteon Vaerzel'}, {'id': 205, 'name': "Celica Anthie'se"}, {'id': 206, 'name': 'Nireza Adrona'}, {'id': 207, 'name': 'Strawberry Icecream'}, {'id': 208, 'name': 'Leah Tribal'}, {'id': 209, 'name': 'Saeri Imaen'}, {'id': 210, 'name': 'Nireza Adrona'}, {'id': 211, 'name': 'Felix Armstrong'}, {'id': 212, 'name': 'Saffran Saeunn'}, {'id': 213, 'name': 'Neo Sanguine'}, {'id': 214, 'name': 'Shuz Ardor'}, {'id': 215, 'name': 'Olivia Ambrosia'}, {'id': 216, 'name': 'Amplified Mayhem'}, {'id': 217, 'name': 'Soul Borger'}, {'id': 218, 'name': 'Carbuncle'}, {'id': 219, 'name': 'Demi-Bahamut'}, {'id': 220, 'name': 'Ifrit-Egi'}, {'id': 221, 'name': 'Garuda-Egi'}, {'id': 222, 'name': 'Titan-Egi'}, {'id': 223, 'name': 'Phoenix'}]}, 'startTime': 1718134438936, 'fights': [{'name': 'Bahamut Prime', 'kill': False, 'lastPhase': 3, 'bossPercentage': 62.1, 'friendlyPlayers': [10, 9, 8, 7, 6, 5, 4, 3, 1], 'encounterID': 1060}, {'name': 'Bahamut Prime', 'kill': False, 'lastPhase': 1, 'bossPercentage': 4.82, 'friendlyPlayers': [10, 9, 8, 7, 6, 5, 4, 3, 1], 'encounterID': 1060}, {'name': 'Bahamut Prime', 'kill': False, 'lastPhase': 3, 'bossPercentage': 59.46, 'friendlyPlayers': [10, 9, 8, 7, 6, 5, 4, 3, 1], 'encounterID': 1060}, {'name': 'Bahamut Prime', 'kill': False, 'lastPhase': 4, 'bossPercentage': 30.77, 'friendlyPlayers': [10, 9, 8, 7, 6, 5, 4, 3, 1], 'encounterID': 1060}, {'name': 'Bahamut Prime', 'kill': False, 'lastPhase': 2, 'bossPercentage': 21.22, 'friendlyPlayers': [10, 9, 8, 7, 6, 5, 4, 3, 1], 'encounterID': 1060}, {'name': 'Bahamut Prime', 'kill': False, 'lastPhase': 1, 'bossPercentage': 81.31, 'friendlyPlayers': [10, 9, 8, 7, 6, 5, 4, 3, 1], 'encounterID': 1060}, {'name': 'Bahamut Prime', 'kill': False, 'lastPhase': 3, 'bossPercentage': 52.02, 'friendlyPlayers': [10, 9, 8, 7, 6, 5, 4, 3, 1], 'encounterID': 1060}, {'name': 'Bahamut Prime', 'kill': False, 'lastPhase': 2, 'bossPercentage': 0.01, 'friendlyPlayers': [10, 217, 216, 8, 215, 6, 5, 4, 3], 'encounterID': 1060}, {'name': 'Bahamut Prime', 'kill': False, 'lastPhase': 3, 'bossPercentage': 50.55, 'friendlyPlayers': [10, 217, 216, 8, 215, 6, 5, 4, 3], 'encounterID': 1060}, {'name': 'Bahamut Prime', 'kill': False, 'lastPhase': 4, 'bossPercentage': 52.46, 'friendlyPlayers': [27, 10, 217, 216, 8, 215, 6, 5, 4, 3], 'encounterID': 1060}, {'name': 'Bahamut Prime', 'kill': False, 'lastPhase': 3, 'bossPercentage': 59.82, 'friendlyPlayers': [10, 217, 216, 8, 215, 6, 5, 4, 3], 'encounterID': 1060}, {'name': 'Bahamut Prime', 'kill': False, 'lastPhase': 5, 'bossPercentage': 8.65, 'friendlyPlayers': [27, 10, 217, 216, 8, 215, 6, 5, 4, 3], 'encounterID': 1060}, {'name': 'Bahamut Prime', 'kill': False, 'lastPhase': 2, 'bossPercentage': 0.01, 'friendlyPlayers': [10, 217, 216, 8, 215, 6, 5, 4, 3], 'encounterID': 1060}, {'name': 'Bahamut Prime', 'kill': False, 'lastPhase': 3, 'bossPercentage': 53.76, 'friendlyPlayers': [10, 217, 216, 8, 215, 6, 5, 4, 3], 'encounterID': 1060}]}}}}
"""
mockReport = ast.literal_eval(jsonString)

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
    "Month Day, Year" format, and a list of fights.
  """
  flattenedReport = reportData.get("data").get("reportData").get("report")

  actorList = flattenedReport.get("masterData").get("actors")

  startTimeUNIX = flattenedReport.get("startTime") // 1000 #millisecond precision
  startTimeString = datetime.fromtimestamp(startTimeUNIX).strftime("%B %d, %Y")

  fightsList = flattenedReport.get("fights")

  rankingsList = flattenedReport.get("rankings").get("data")

  return actorList, startTimeString, fightsList, rankingsList

def generateEmbedFromReport(reportData: dict, link: str, description: str) -> Embed:
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
  print(reportData)
  if "errors" in reportData:
     raise ReportDataError("The received report data is not correctly formatted or missing.")
  # print(reportData.get("data").get("reportData"))
  actors, dateString, fights, rankings = extractReportFields(reportData)
  fightsNameSet =set([fight.get("name") for fight in fights])
  print(fights)
  print(isFightUltimate(fight) for fight in fights)
  titleFight = ""
  if len(fightsNameSet) == 1:
     titleFight = next(iter(fightsNameSet))
  else:
    titleFight = "Multiple Fights"
    description = "Fights: " + ", ".join([fightName for fightName in fightsNameSet])

  pullTotal = len(fights)

  reportEmbed = Embed(title=titleFight + " - " + dateString)
  reportEmbed.description = description
  reportEmbed.add_field(name="Pulls", value=pullTotal, inline=False)
  reportEmbed.add_field(name="Clear?", value=True, inline=True)
  reportEmbed.url = link

  print(dateString)

  return reportEmbed

if __name__ == "__main__":
   generateEmbedFromReport(mockReport, "lol")