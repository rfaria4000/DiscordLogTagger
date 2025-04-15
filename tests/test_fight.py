import pytest
from fight import Fight
from unittest.mock import patch
from typing import NamedTuple

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
    dummy_actor_list = [{"id": 12, "name": "Jim", "subType": "Warrior"}]
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
    class mock_job_info(NamedTuple):
      priority: int
    with patch("fight.jobinfo") as mock:
      mock.emojiDict = {
        "Paladin": mock_job_info(2),
        "Sage": mock_job_info(1),
        "Reaper": mock_job_info(3),
      }
      yield mock
  
  def test_fails_without_friendly_players(self):
    fight = Fight({}, [])
    with pytest.raises(Exception):
      assert(fight.partyMembers == [])
  
  def test_succeeds_with_empty_friendly_players(self):
    fight = Fight({"friendlyPlayers": []}, [])
    assert(fight.partyMembers == [])

  def test_fails_without_actor_data(self, sample_fight_data):
    fight = Fight(sample_fight_data, [])
    with pytest.raises(Exception):
      fight.partyMembers

  def test_fails_with_mismatched_player_ids(self, sample_actor_data):
    fight = Fight({"friendlyPlayers": [5, 6, 7, 8]}, sample_actor_data)
    with pytest.raises(Exception):
      fight.partyMembers

  def test_skips_past_limit_break(self, sample_fight_data, sample_actor_data):
    fight = Fight(sample_fight_data, sample_actor_data)
    names = [member.name for member in fight.partyMembers]
    assert len(fight.partyMembers) == 3
    assert "Tabu" not in names

  def test_player_parses_default_without_rankings(self,
                                                  sample_fight_data,
                                                  sample_actor_data):
    fight = Fight(sample_fight_data, sample_actor_data)
    parses = [member.parse for member in fight.partyMembers]
    assert len(set(parses)) == 1
    assert parses[0] == -1
  
  def test_list_is_sorted_according_to_priority(self,
                                                sample_fight_data,
                                                sample_actor_data):
    fight = Fight(sample_fight_data, sample_actor_data)
    assert fight.partyMembers[0].name == "Violet"
    assert fight.partyMembers[1].name == "Neri" 
    assert fight.partyMembers[2].name == "Estellia"

  def test_results_cached(self, sample_fight_data, sample_actor_data):
    fight = Fight(sample_fight_data, sample_actor_data)
    fight.partyMembers
    assert "partyMembers" in fight.__dict__
  
  def test_succeeds_with_ranking_data(self, 
                                      sample_fight_data, 
                                      sample_actor_data, 
                                      sample_ranking_data):
    fight = Fight(sample_fight_data, sample_actor_data, sample_ranking_data)
    assert len(fight.partyMembers) == 3
    assert fight.partyMembers[0].parse == 70
    assert fight.partyMembers[0].job == "Sage"
    assert fight.partyMembers[1].parse == 20
    assert fight.partyMembers[1].job == "Paladin"
    assert fight.partyMembers[2].parse == 99
    assert fight.partyMembers[2].job == "Reaper"

# If I'm thinking about entry/exit points for Fight:
# test comparison (for each possible if)
# change secondsElapsed/timeElapsed to set variables inside the class
# Test bestParse for a few ranked fights
# Test emojis/colors for a multitude of best parses
# Cursory tests on thumbnail
# Test party members/parses to match website
# To embed works based on certain dummy test data