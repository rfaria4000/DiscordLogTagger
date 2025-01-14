class Report:
  """
  Represents a combat report on FFLogs.
  """
  def __init__(self, reportData: dict[str, dict]):
    self.reportData = reportData
    self.unpack_data()

  def unpack_data(self):
    report = self.reportData["data"]["reportData"]["report"]
    self.code = report["code"]
    self.author = report["owner"]["name"]
    self.actorData = report["masterData"]["actors"]
    self.fightData = report["fights"]
    self.startTime = report["startTime"] // 1000 #millisecond precision

  # I'm going to need some sort of filter function to grab specific things

if __name__ == "__main__":
  import json, os

  dir = os.path.dirname(__file__)
  mockReportData = None
  with open(os.path.join(dir, "tests/test_data/ultimate.json"), "r") as f:
    mockReportData = json.load(f)
  testReport = Report(mockReportData)
  print(testReport)