import pytest
from fight import Fight
from unittest.mock import patch

class TestInit():
  def test_init_succeeds_with_placeholders(self):
    fight = Fight({}, [])
    assert(True)

  def test_init_sets_fight_data_when_empty(self):
    fight = Fight({}, [])
    assert fight.fightData == {}

  def test_fails_without_arguments(self):
    with pytest.raises(Exception):
      fight = Fight()
  
  def test_init_sets_fight_data_when_populated(self):
    dummy_fight_data = {"name": "Zeromus", "id": 1}
    fight = Fight(dummy_fight_data, [])
    assert fight.fightData == dummy_fight_data

  def test_inherits_fields_from_fight_data(self):
    dummy_fight_data = {"name": "Zeromus", "id": 1}
    fight = Fight(dummy_fight_data, [])
    assert hasattr(fight, "name")
    assert hasattr(fight, "id")
    assert fight.name == "Zeromus"
    assert fight.id == 1

  def test_init_sets_actor_data(self):
    dummy_actor_list = [{"id": 12, "name": "Bob", "subType": "Warrior"}]
    fight = Fight({}, dummy_actor_list)
    assert len(fight.actorData) == 1
    assert fight.actorData == dummy_actor_list

  def test_init_sets_ranking_data_when_missing(self):
    fight = Fight({}, [])
    assert (fight.rankingData == {})

  def test_init_sets_ranking_data_when_populated(self):
    dummy_ranking_data = {"Bob": 93}
    fight = Fight({}, [], dummy_ranking_data)
    assert fight.rankingData == dummy_ranking_data

  def test_init_succeeds_with_valid_data(self, extreme_fight_all_data):
    fight_data, actor_data, ranking_data = extreme_fight_all_data
    fight = Fight(fight_data, actor_data, ranking_data)
    assert fight.name == "Zeromus"
    assert fight.id == 10
    assert fight.kill == True
    assert fight.difficulty == 100
    assert fight.lastPhase == 0
    assert fight.encounterID == 1070
    assert fight.fightData == fight_data
    assert fight.actorData == actor_data
    assert fight.rankingData == ranking_data

class TestPartyMembers():
  @pytest.fixture(autouse=True)
  def mock_job_info(self):
    with patch("data.jobinfo") as mock_job_info:
      mock_job_info.emojiDict = {
        "Paladin": {"priority": 1},
        "Sage": {"priority": 2},
        "Reaper": {"priority": 3},
      }
      yield mock_job_info
  
  def test_empty_players(self):
    pass

# If I'm thinking about entry/exit points for Fight:
# test unpack party members
# test comparison (for each possible if)
# change secondsElapsed/timeElapsed to set variables inside the class
# Test bestParse for a few ranked fights
# Test emojis/colors for a multitude of best parses
# Cursory tests on thumbnail
# Test party members/parses to match website
# To embed works based on certain dummy test data