from discord import Embed

class ReportDataError(Exception):
    """The received reportData is not correctly formatted or missing."""

def generateEmbedFromReport(reportData: dict) -> Embed:
  """
  Generates a Discord Embed from report data acquired from an FFLogs query.
  
  Args:
    `reportData`: A dict representing a json object containing reportData.

  Returns:
    A Discord Embed featuring relevant infomation such as the name of the fight,
    date, number of pulls, whether the fight was cleared, etc.
  
  Raises:
    `ReportDataError`: the reportData is not correctly formatted or missing.
  """
  if "errors" in reportData:
     raise ReportDataError("The received report data is not correctly formatted or missing.")
  print(reportData)