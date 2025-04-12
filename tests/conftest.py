import pytest
import json
import os

@pytest.fixture
def extreme_fight_all_data():
  dir = os.path.dirname(__file__)
  mock_exteme_data = None
  with open(os.path.join(dir, "test_data/extreme.json"), "r") as f:
    mock_exteme_data = json.load(f)

  report_data = mock_exteme_data["data"]["reportData"]["report"]
  fight_data = report_data["fights"][9]
  actor_data = report_data["masterData"]["actors"]
  ranking_data = report_data["rankings"]["data"][0]
  return (fight_data, actor_data, ranking_data)

@pytest.fixture
def sample_fight_data():
  return {
    "friendlyPlayers": [1, 2, 3, 4],
  }

@pytest.fixture
def sample_actor_data():
  return [
    {"name": "Neri", "id": 1, "subType": "Paladin"},
    {"name": "Violet", "id": 2, "subType": "Sage"},
    {"name": "Estellia", "id": 3, "subType": "Reaper"},
    {"name": "Tabu", "id": 4, "subType": "LimitBreak"},
  ]

@pytest.fixture
def sample_ranking_data():
  return {
    "roles": {
       "tanks": {
         "characters": [{"name": "Neri", "rankPercent": 20}]
       },
       "healers": {
         "characters": [{"name": "Violet", "rankPercent": 70}]
       },
       "dps": {
         "characters": [{"name": "Estellia", "rankPercent": 99}]
       }
    }
  }