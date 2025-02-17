import requests
from data.query import fightQuery

class FFLogsSession:
  publicEndpoint = "https://www.fflogs.com/api/v2/client"
  authEndpoint = "https://www.fflogs.com/oauth/authorize"
  tokenEndpoint = "https://www.fflogs.com/oauth/token"
  redirectURL = "https://localhost:8080"

  data = {
    'grant_type': 'client_credentials',
  }

  def __init__(self, client_id, client_secret) -> None:
    """Fetches an authentication token given a client ID and secret."""
    session = requests.Session()
    session.auth = (client_id, client_secret)
    authResponse = session.post(self.tokenEndpoint, data=self.data).json()
    self.authHeader = {'Authorization': f'Bearer {authResponse["access_token"]}'}

  def getReportData(self, code: str) -> object:
    """Returns fight data from given FFLogs report code."""
    variables = {
    "fightCode": f"{code}"
    }

    response = requests.post(self.publicEndpoint, 
                           headers=self.authHeader,
                           json={"query": fightQuery, "variables": variables}
                           ).json()
    return response