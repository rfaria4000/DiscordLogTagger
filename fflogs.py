import requests

# publicEndpoint = "https://www.fflogs.com/api/v2/client"
# authEndpoint = "https://www.fflogs.com/oauth/authorize"
# tokenEndpoint = "https://www.fflogs.com/oauth/token"
# redirectURL = "https://localhost:8080"

# fightQuery = """
# query getReport($fightCode: String){
# 	reportData{
# 		report(code: $fightCode){
# 			masterData{
# 				actors{
# 					id
# 					name
# 				}
# 			}
			
# 			startTime
			
# 			fights(killType: Encounters){
# 				name
# 				kill
# 				lastPhase
# 				bossPercentage
# 				friendlyPlayers
# 				encounterID
# 			}
# 		}
# 	}
# }
# """

# headers = {}
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
    self.client_id = client_id
    self.cliend_secret = client_secret
    session = requests.Session()
    session.auth = (client_id, client_secret)
    authResponse = session.post(self.tokenEndpoint, data=self.data).json()
    self.authHeader = {'Authorization': f'Bearer {authResponse["access_token"]}'}

  def getReportData(self, code: str) -> object:
    """Returns fight data from given FFLogs report code."""

    variables = {
    "fightCode": f"{code}"
    }

    response = requests.post('https://www.fflogs.com/api/v2/client', 
                           headers=self.authHeader,
                           json={"query": self.fightQuery, "variables": variables}
                           ).json()
    
    return response

    # print(self.session.auth)

    # response = requests.post('https://www.fflogs.com/api/v2/client', 
    #                        headers=headers,
    #                        json={"query": fightQuery, "variables": variables}
    #                        ).json()
    # return self.session.post(self.publicEndpoint,json={"query": self.fightQuery, "variables": variables}).json()
