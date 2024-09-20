import os
import json
import pytest
import embed

def get_test_data(filter) -> list:
  test_data = []
  dir = os.path.dirname(__file__)
  with os.scandir(os.path.join(dir, 'test_data/')) as test_folder_iterator:
    for test_entry in test_folder_iterator:
      if filter(test_entry.name):
        with open(test_entry.path) as test:
          test_data.append(json.load(test))
  
  return test_data

@pytest.mark.parametrize("test_data", get_test_data(lambda test: True))
class TestEmbed:  
  @pytest.fixture(scope="function", autouse=True)
  def setup_and_teardown(self, test_data):
    print("setup")
    self.report = test_data
    self.code = self.report["data"]["reportData"]["report"]["code"]
    self.link = f"https://www.fflogs.com/reports/{self.code}"
    self.embed = embed.generateEmbed(self.report, self.link)
    
    yield
    
    print("teardown")
    del self.report, self.code, self.link, self.embed

  def test_embed_author(self, test_data):
    print("inside test")
    reportOwner = self.report["data"]["reportData"]["report"]["owner"]["name"]
    assert self.embed.author.name == f"Uploaded by {reportOwner}"

  def test_embed_link(self):
    assert self.embed.url == self.link

  def test_embed_time(self):
    reportTime = self.report["data"]["reportData"]["report"]["startTime"]//1000
    assert (str(reportTime) in self.embed.title)
  