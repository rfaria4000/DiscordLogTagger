import os, json
import embed

class TestMulti:
  def setup_method(self, method):
    print(f"Setting up {method}")
    dir = os.path.dirname(__file__)
    with open(os.path.join(dir,"test_data/extreme.json")) as f:
      self.report = json.load(f)
    self.link = "https://www.fflogs.com/reports/rT4xKXkcLgbAqa1d"
    self.embed = embed.generateEmbed(self.report, self.link)

  def teardown_method(self, method):
    print(f"Tearing down {method}")
    del self.report
    del self.link
    del self.embed

  def test_multi_name(self):
    pass
  
  def test_multi_field_names(self):
    pass

  def test_multi_pull_count(self):
    pass

  def test_multi_color(self):
    pass

  def test_multi_thumbnail(self):
    pass