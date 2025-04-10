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