import os
import json
import pytest
import report

def get_test_data(filter) -> list:
  test_data = []
  dir = os.path.dirname(__file__)
  with os.scandir(os.path.join(dir, 'test_data/')) as test_folder_iterator:
    for test_entry in test_folder_iterator:
      if filter(test_entry.name):
        with open(test_entry.path) as test:
          test_data.append(json.load(test))
  
  return test_data

def get_report_code(report) -> str:
  return report["data"]["reportData"]["report"]["code"]

def get_actors(report) -> list:
  return report["data"]["reportData"]["report"]["masterData"]["actors"]

def get_rankings(report) -> list:
  return report["data"]["reportData"]["report"]["rankings"]["data"]

@pytest.mark.parametrize("test_data", get_test_data(lambda test: True))
class TestEmbed:  
  @pytest.fixture(scope="function", autouse=True)
  def setup_and_teardown(self, test_data):
    print("setup")
    self.report = test_data
    self.code = get_report_code(self.report)
    self.link = f"https://www.fflogs.com/reports/{self.code}"
    self.embed = report.Report(self.report).toEmbed(self.link)
    yield
    
    print("teardown")
    del self.report, self.code, self.link, self.embed

  def test_embed_author(self, test_data):
    print("inside test")
    reportOwner = self.report["data"]["reportData"]["report"]["owner"]["name"]
    assert self.embed.author.name == f"Uploaded by {reportOwner}"

  def test_embed_link(self):
    assert self.embed.url.startswith(self.link)

  def test_embed_time(self):
    reportTime = self.report["data"]["reportData"]["report"]["startTime"]//1000
    assert (str(reportTime) in self.embed.title)
  