import os, json
import embed

FIELD_PULLS = 0
FIELD_BEST_PULL = 1
FIELD_CLEAR_PULLS = 2

class TestMulti:
  def setup_method(self, method):
    print(f"Setting up {method}")
    dir = os.path.dirname(__file__)
    with open(os.path.join(dir,"test_data/extreme.json")) as f:
      self.report = json.load(f)
    self.link = "https://www.fflogs.com/reports/rT4xKXkcLgbAqa1d"
    self.embed = embed.generateEmbed(self.report, self.link)
    self.fightList = self.report["data"]["reportData"]["report"]["fights"]

  def teardown_method(self, method):
    print(f"Tearing down {method}")
    del self.report
    del self.link
    del self.embed
    del self.fightList

  def test_multi_name(self):
    firstFightName = self.fightList[0]["name"]
    assert(all(firstFightName == x["name"] for x in self.fightList)
           and self.embed.title.startswith("🔷 " + firstFightName))
  
  def test_multi_field_name_pulls(self):
    assert(self.embed.fields[FIELD_PULLS].name == "Pulls")

  def test_multi_field_name_best_pull(self):
    assert(self.embed.fields[FIELD_BEST_PULL].name == "Best Pull")

  def test_multi_field_name_clear_pulls(self):
    assert(self.embed.fields[FIELD_CLEAR_PULLS].name == "Clear Pulls?")

  def test_multi_pull_count(self):
    firstFightName = self.fightList[0]["name"]
    pullCount = len(list(filter(lambda x: x["name"] == firstFightName, 
                                self.fightList)))
    assert(int(self.embed.fields[FIELD_PULLS].value) == pullCount)

  def test_multi_color(self):
    for emoji in reversed(embed.PULL_EMOJIS):
      if emoji in self.embed.fields[FIELD_CLEAR_PULLS].value:
        emojiIndex = embed.PULL_EMOJIS.index(emoji)
        assert(self.embed.color.value == embed.PULL_HEXCODES[emojiIndex])
        break

  def test_multi_thumbnail(self):
    firstFightID = self.fightList[0]["encounterID"]
    assert(str(firstFightID) in self.embed.thumbnail.url)