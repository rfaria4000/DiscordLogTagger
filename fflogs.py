import requests

publicEndpoint = "https://www.fflogs.com/api/v2/client"
authEndpoint = "https://www.fflogs.com/oauth/authorize"
tokenEndpoint = "https://www.fflogs.com/oauth/token"
redirectURL = "https://localhost:8080"

fightQuery = """
query getReport($fightCode: String){
	reportData{
		report(code: $fightCode){
			masterData{
				actors{
					id
					name
				}
			}
			
			startTime
			
			fights(killType: Encounters){
				name
				kill
				lastPhase
				bossPercentage
				friendlyPlayers
				encounterID
			}
		}
	}
}
"""

headers = {}
# session = requests.Session()

def authorizeFFLogs(client_id, client_secret) -> None:
  data = {
    'grant_type': 'client_credentials',
  }

  authResponse = requests.post(tokenEndpoint, data=data, auth=(client_id, client_secret)).json()
  print(authResponse)

  # print(session.post(tokenEndpoint, data=data, auth=(client_id, client_secret)).json())

  headers = {
    'Authorization': f'Bearer {authResponse["access_token"]}',
  }



def getFFLogsFightData(code: str) -> object:
  """Returns fight data from given FFLogs report code."""
  variables = {
    "fightCode": f"{code}"
  }

  response = requests.post('https://www.fflogs.com/api/v2/client', 
                           headers=headers,
                           json={"query": fightQuery, "variables": variables}
                           ).json()
  return response

class FFLogsSession:
  publicEndpoint = "https://www.fflogs.com/api/v2/client"
  authEndpoint = "https://www.fflogs.com/oauth/authorize"
  tokenEndpoint = "https://www.fflogs.com/oauth/token"
  redirectURL = "https://localhost:8080"

  data = {
    'grant_type': 'client_credentials',
  }

  fightQuery = """
  query getReport($fightCode: String){
    reportData{
      report(code: $fightCode){
        masterData{
          actors{
            id
            name
          }
        }
        
        startTime
        
        fights(killType: Encounters){
          name
          kill
          lastPhase
          bossPercentage
          friendlyPlayers
          encounterID
        }
      }
    }
  }
  """

  def __init__(self, client_id, client_secret) -> None:
    session = requests.Session()
    session.auth = (client_id, client_secret)
    authResponse = session.post(self.tokenEndpoint, data=self.data).json()
    session.headers.update({'Authorization': f'Bearer {authResponse["access_token"]}'})
    self.session = session
    print(authResponse)

  def getReportData(self, code: str) -> object:
    """Returns fight data from given FFLogs report code."""
    print(self.session)