import os, json
import embed

class TestSingle:
  def setup_method(self, method):
    print(f"Setting up {method}")
    dir = os.path.dirname(__file__)
    with open(os.path.join(dir,"test_data/extreme.json")) as f:
      self.report = json.load(f)
    self.link = "https://www.fflogs.com/reports/rT4xKXkcLgbAqa1d#fight=15"
    self.embed = embed.generateEmbed(self.report, self.link)

  def teardown_method(self, method):
    print(f"Tearing down {method}")
    del self.report
    del self.link
    del self.embed

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