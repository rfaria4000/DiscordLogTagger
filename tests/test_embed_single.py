import pytest
import embed
import data.emoji
from .test_embed import get_test_data, get_report_code, get_actors, get_rankings

FFLOGS_TEMPLATE = "https://www.fflogs.com/reports/{0}#fight={1}"
FIELD_STATUS = 0
FIELD_PARTY = 1
FIELD_PARSES = 2
SIZE_OF_EMBED_WITH_PARSE_DATA = 3

test_data = get_test_data(lambda test: True)

def get_report_fight_ids_dict(test_data):
  report_fights = {}
  for report in test_data:
    fights = report["data"]["reportData"]["report"]["fights"]
    fight_ids = (list(map(lambda fight: fight["id"], fights)))
    report_fights[get_report_code(report)] = fight_ids
  
  return report_fights

def zip_test_data_fights(test_data):
  test_cases = []
  for report in test_data:
    fights = report["data"]["reportData"]["report"]["fights"]
    fight_ids = (list(map(lambda fight: fight["id"], fights)))
    for fight in fight_ids:
      test_cases.append((report, fight))
  
  return test_cases

def get_fight(report: list, id: int) -> dict:
  fights = report["data"]["reportData"]["report"]["fights"]
  for fight in fights:
    if fight["id"] == id:
      return fight
  
  return None

def filterCombinedParses(characterParse: dict) -> bool:
  return "id_2" not in characterParse

report_fights = get_report_fight_ids_dict(test_data)
data_with_fights = zip_test_data_fights(test_data)

@pytest.mark.parametrize("test_data,fight_number", data_with_fights)
class TestSingleAll:
  @pytest.fixture(scope="function", autouse=True)
  def setup_and_teardown(self, test_data, fight_number):
    self.report = test_data
    self.fightID = fight_number
    self.fight = get_fight(self.report, self.fightID)
    self.code = get_report_code(self.report)
    self.link = FFLOGS_TEMPLATE.format(self.code, self.fightID)
    self.embed = embed.generateEmbed(self.report, self.link)
    
    yield
    
    del self.report, self.fightID, self.fight, self.code, self.link, self.embed

  def test_single_name(self):
    assert(self.embed.title.startswith(f"🔸 {self.fight['name']}"))
  
  def test_single_field_name_status(self):
    assert(self.embed.fields[FIELD_STATUS].name == "Status")

  def test_single_field_name_party(self):
    assert(self.embed.fields[FIELD_PARTY].name == "Party")

  def test_single_field_name_parses(self):
    if len(self.embed.fields) == SIZE_OF_EMBED_WITH_PARSE_DATA:
      assert(self.embed.fields[FIELD_PARSES].name == "Parses")

  def test_single_party_members(self):
    actorList = get_actors(self.report)
    for playerID in self.fight["friendlyPlayers"]:
      matchingPlayer = next(actor for actor in actorList 
                            if actor["id"] == playerID)
      if matchingPlayer["name"] in ["Multiple Players", "Limit Break"]: 
        continue
      assert(matchingPlayer["name"] in self.embed.fields[FIELD_PARTY].value)

  def test_single_parses(self):
    if len(self.embed.fields) < SIZE_OF_EMBED_WITH_PARSE_DATA: 
      pytest.skip("No parses displayed.")
    
    rankingList = get_rankings(self.report)
    fightRankings = next(parse for parse in rankingList 
                          if parse["fightID"] == self.fightID)
    
    characterParses = []
    for role in ["tanks","healers", "dps"]:
      characterParses.extend(fightRankings["roles"][role]["characters"])
    
    filteredParses = list(filter(filterCombinedParses, characterParses))
    filteredParses.sort(key=lambda x: data.emoji.emojiDict[x["class"]].priority)
    displayedParses = self.embed.fields[FIELD_PARSES].value.split("\n")
    
    for i in range(len(displayedParses)):
      assert str(filteredParses[i]["rankPercent"]) in displayedParses[i]

  def test_single_color(self):
    pass

  def test_single_thumbnail(self):
    assert(str(self.fight["encounterID"]) in self.embed.thumbnail.url) 

@pytest.mark.parametrize("test_data", test_data)
class TestSingleLast:
  @pytest.fixture(scope="function", autouse=True)
  def setup_and_teardown(self, test_data):
    report_code = get_report_code(test_data)
    link_fight_last = FFLOGS_TEMPLATE.format(report_code, "last")
    link_last_id = FFLOGS_TEMPLATE.format(report_code, 
                                          report_fights[report_code][-1])
    self.embed_fight_last = embed.generateEmbed(test_data, link_fight_last)
    self.embed_last_id = embed.generateEmbed(test_data, link_last_id)

  def test_last_title(self, test_data):
    assert(self.embed_fight_last.title == self.embed_last_id.title)

  def test_last_fields(self):
    assert(self.embed_fight_last.fields == self.embed_last_id.fields)

  def test_last_color(self):
    assert(self.embed_fight_last.color == self.embed_last_id.color)

  def test_last_thumbnail(self):
    assert(self.embed_fight_last.thumbnail.url 
           == self.embed_last_id.thumbnail.url)