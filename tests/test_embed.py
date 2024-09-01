import pytest
import os, json
import embed

# def inc(x: int) -> int:
#   return x + 1

# @pytest.mark.parametrize("number, expected_sum", [(1, 2), (2, 3), (-1, 0)])
# def test_inc(number, expected_sum):
#   assert inc(number) == expected_sum

class TestCompilation:
  def setup_method(self, method):
    print(f"Setting up {method}")
    dir = os.path.dirname(__file__)
    with open(os.path.join(dir,"test_data/compilation.json")) as f:
      self.report = json.load(f)
    self.link = "https://www.fflogs.com/reports/CRh38LcT7BzAdHyr"
    self.embed = embed.generateEmbed(self.report, self.link)

  def teardown_method(self, method):
    print(f"Tearing down {method}")
    del self.report
    del self.link
    del self.embed

  def test_compilation_name(self):
    # compilationEmbed = embed.generateEmbed(compilation_report, compilation_link)
    assert self.embed.title.startswith("💠 Multiple Fights - ")

  def test_compilation_author(self):
    reportOwner = self.report["data"]["reportData"]["report"]["owner"]["name"]
    assert self.embed.author.name == f"Uploaded by {reportOwner}"

  def test_compilation_link(self):
    assert self.embed.url == self.link

  def test_compilation_time(self):
    reportTime = self.report["data"]["reportData"]["report"]["startTime"]//1000
    assert (str(reportTime) in self.embed.title)

  def test_compilation_fields(self):
    assert "Notable Fights" == self.embed.fields[0].name
    notableFightNames = self.embed.fields[0].value.split(",")
    for i in range(1, len(self.embed.fields)):
      assert self.embed.fields[i].name.startswith(notableFightNames[i-1])

  #TODO: Figure out how to test color and parametrize compilation test

# Look into mocking for a variety of test datas - need all three types