import pytest
import embed
from .test_embed import get_test_data

test_data = get_test_data(lambda test: True)

def get_report_fight_ids(test_data):
  fight_count = []
  for report in test_data:
    fights = report["data"]["reportData"]["report"]["fights"]
    fight_count.append(list(map(lambda fight: fight["id"], fights)))
  
  return fight_count

print(get_report_fight_ids(test_data))

@pytest.mark.parametrize("test_data", test_data)
class TestSingle:
  @pytest.fixture(scope="function", autouse=True)
  def setup_and_teardown(self, test_data):
    # print("setup")
    self.report = test_data
    self.code = self.report["data"]["reportData"]["report"]["code"]
    self.link = f"https://www.fflogs.com/reports/{self.code}#fight=1"
    self.embed = embed.generateEmbed(self.report, self.link)
    
    yield
    
    # print("teardown")
    del self.report, self.code, self.link, self.embed

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