import pytest
import os, json
import embed

def inc(x: int) -> int:
  return x + 1

@pytest.mark.parametrize("number, expected_sum", [(1, 2), (2, 3), (-1, 0)])
def test_inc(number, expected_sum):
  assert inc(number) == expected_sum

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
    assert self.embed.title.startswith("💠 Multiple Fights -")

  def test_compilation_author(self):
    assert self.embed.author.name == "Uploaded by DSXXI"

  def test_compilation_link(self):
    assert self.embed.url == self.link
# Look into mocking for a variety of test datas - need all three types