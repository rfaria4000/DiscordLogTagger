import pytest
import embed
from .test_embed import get_test_data, get_report_code

FFLOGS_TEMPLATE = "https://www.fflogs.com/reports/{0}#fight={1}"

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

report_fights = get_report_fight_ids_dict(test_data)
data_with_fights = zip_test_data_fights(test_data)

@pytest.mark.parametrize("test_data,fight_number", data_with_fights)
class TestSingleAll:
  @pytest.fixture(scope="function", autouse=True)
  def setup_and_teardown(self, test_data, fight_number):
    self.report = test_data
    self.code = get_report_code(self.report)
    self.link = FFLOGS_TEMPLATE.format(self.code, fight_number)
    self.embed = embed.generateEmbed(self.report, self.link)
    
    yield
    
    del self.report, self.code, self.link, self.embed

  # @pytest.mark.parametrize("fight_number", report_fights[get_report_code(self.report)])
  def test_single_name(self):
    pass
  
  def test_single_field_names(self):
    pass

  def test_single_party_members(self):
    pass

  def test_single_parses(self):
    pass

  def test_single_color(self):
    pass

  def test_single_thumbnail(self):
    pass

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
    assert self.embed_fight_last.title == self.embed_last_id.title

  def test_last_field_names(self):
    assert self.embed_fight_last.fields == self.embed_last_id.fields
    pass

  def test_last_party_members(self):
    pass

  def test_last_parses(self):
    pass

  def test_last_color(self):
    pass

  def test_last_thumbnail(self):
    pass