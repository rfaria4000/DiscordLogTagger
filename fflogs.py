from requests_oauthlib import OAuth2Session
import os

import requests

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

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

def authorizeFFLogs(client_id, client_secret):
  data = {
    'grant_type': 'client_credentials',
  }

  authResponse = requests.post(tokenEndpoint, data=data, auth=(client_id, client_secret)).json()
  print(authResponse)

  headers = {
    'Authorization': f'Bearer {authResponse["access_token"]}',
  }

  variables = {
    "fightCode": "7Myb4A6dDq1HnWvc"
  }

  response = requests.post('https://www.fflogs.com/api/v2/client', 
                           headers=headers,
                           json={"query": fightQuery, "variables": variables}
                           ).json()
  print(response.text)
  pass