import os, json
import embed

class TestCompilation:
  def setup_method(self, method):
    print(f"Setting up {method}")
    dir = os.path.dirname(__file__)
    with open(os.path.join(dir,"test_data/compilation.json")) as f:
      self.report = json.load(f)
    self.link = "https://www.fflogs.com/reports/CRh38LcT7BzAdHyr"
    self.embed = embed.generateEmbed(self.report, self.link)
    self.fightList = self.report["data"]["reportData"]["report"]["fights"]

  def teardown_method(self, method):
    print(f"Tearing down {method}")
    del self.report
    del self.link
    del self.embed
    del self.fightList

  def test_compilation_name(self):
    assert self.embed.title.startswith("💠 Multiple Fights - ")

  def test_compilation_field_names(self):
    assert "Notable Fights" == self.embed.fields[0].name
    notableFightNames = self.embed.fields[0].value.split(",")
    for i in range(1, len(self.embed.fields)):
      fightName = notableFightNames[i-1]
      assert self.embed.fields[i].name.startswith(fightName)
  
  def test_compilation_field_pull_counts(self):
    notableFightNames = self.embed.fields[0].value.split(",")
    for i in range(1, len(self.embed.fields)):
      fightName = notableFightNames[i-1]
      fightCount = len([fight for fight in self.fightList 
                        if fight["name"] == fightName])
      assert str(fightCount) in self.embed.fields[i].name

  def test_compilation_color(self):
    for emoji in reversed(embed.PULL_EMOJIS):
      if emoji in self.embed.fields[1].value:
        emojiIndex = embed.PULL_EMOJIS.index(emoji)
        assert self.embed.color.value == embed.PULL_HEXCODES[emojiIndex]
        break

  def test_compilation_thumbnail(self):
    highlightFight = self.embed.fields[0].value.split(",")[0]
    fightEncounterID = next(fight for fight in self.fightList 
                            if fight["name"] == highlightFight)["encounterID"]
    assert str(fightEncounterID) in self.embed.thumbnail.url