import pytest
from fight import Fight
from unittest.mock import patch, PropertyMock
from typing import NamedTuple

@pytest.fixture
def empty_fight():
  return Fight({}, [])

class TestInit:
  def test_init_succeeds_with_placeholders(self):
    fight = Fight({}, [])
    assert(True)

  def test_init_sets_fight_data_when_empty(self, empty_fight):
    assert empty_fight.fightData == {}

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

  def test_init_sets_ranking_data_when_missing(self, empty_fight):
    assert (empty_fight.rankingData == {})

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

class TestPartyMembers:
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
  
  def test_fails_without_friendly_players(self, empty_fight):
    with pytest.raises(Exception):
      assert(empty_fight.partyMembers == [])
  
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

class TestStringRepresentation:
  # TODO: Handle this gracefully
  def test_fails_without_properties(self, empty_fight):
    with pytest.raises(AttributeError):
      str(empty_fight)

  def test_succeeds_with_overriden_properties(self):
    fight_data = {
      "id": 1,
      "name": "Dragonsong's Reprise",
    }
    fight = Fight(fight_data, [])
    
    with (
      patch.object(Fight, 
                   "fightTier", 
                   new_callable=PropertyMock) as mock_tier,
      patch.object(Fight, 
                   "completionStatus", 
                   new_callable=PropertyMock) as mock_completion_status
    ):
      mock_tier.return_value = "3"
      mock_completion_status.return_value = "Clear in 18:41"

      assert str(fight) == ("Overview for fight 1:\n"
                            "  Name: Dragonsong's Reprise\n"
                            "  Difficulty: 3\n"
                            "  Status: Clear in 18:41\n")

class TestEquality:
  def test_comparison_to_non_fight(self, empty_fight):
    # with pytest.raises(NotImplemented):
    assert empty_fight != {}

  def test_empty_fights_equal(self):
    fightOne = Fight({}, [])
    fightTwo = Fight({}, [])
    assert fightOne == fightTwo
    assert fightOne is not fightTwo

  def test_equal_fights(self,
                        sample_fight_data,
                        sample_actor_data,
                        sample_ranking_data):
    fightOne = Fight(sample_fight_data, sample_actor_data, sample_ranking_data)
    fightTwo = Fight(sample_fight_data, sample_actor_data, sample_ranking_data)
    assert fightOne == fightTwo
    assert fightOne is not fightTwo

  def test_different_fight_data(self, empty_fight):
    fight = Fight({"id": 3}, [])
    assert empty_fight != fight

  def test_different_actor_data(self, empty_fight):
    fight = Fight({},  [{"name": "Jun'o"}])
    assert empty_fight != fight

  def test_different_ranking_data(self):
    fightOne = Fight({}, [], {})
    fightTwo = Fight ({}, [], {"name": "Gatita"})

    assert fightOne != fightTwo

class TestComparison:
  @pytest.fixture(autouse=True)
  def mock_dependencies(self):
    def mock_property(prop):
      return property(lambda self: self.fightData[prop],
                      lambda self, value: None)
    
    with (
      patch.object(Fight, "fightTier", mock_property("fightTier")),
      patch.object(Fight, "timeElapsed", mock_property("timeElapsed"))
    ):
      yield 

  def test_assignment(self):
    fight = Fight({"fightTier": 3, "timeElapsed": 900}, [])
    assert fight.fightTier == 3
    assert fight.timeElapsed == 900

class TestFightTier:
  @pytest.fixture(autouse=True)
  def mock_fight_tier(self):
    with patch("fight.FightTier") as mock_tiers:
      mock_tiers.ULTIMATE = "Ultimate"
      mock_tiers.SAVAGE = "Savage"
      mock_tiers.RANKED = "Ranked"
      mock_tiers.UNRANKED = "Unranked"
      yield mock_tiers
  
  # TODO: Handle this gracefully
  def test_empty_fight_fails(self, empty_fight):
    with pytest.raises(Exception):
      empty_fight.fightTier

  def test_ultimate(self):
    fight = Fight({"lastPhase": 1}, [])
    assert fight.fightTier == "Ultimate"

  def test_savage(self):
    fight = Fight({"lastPhase": 0, "difficulty": 101}, [])
    assert fight.fightTier == "Savage"

  def test_ultimate_despite_savage_difficulty(self):
    fight = Fight({"lastPhase": 1, "difficulty": 101}, [])
    assert fight.fightTier == "Ultimate"

  def test_ranked(self):
    fight = Fight({"lastPhase": 0, "difficulty": 100}, [], {"name": "Nyx"})
    assert fight.fightTier == "Ranked"

  def test_unranked(self):
    fight = Fight({"lastPhase": 0, "difficulty": 100}, [])
    assert fight.fightTier == "Unranked"

  # TODO: Handle these gracefully as well
  def test_missing_phase_fails(self):
    fight = Fight({"difficulty": 101}, [])
    with pytest.raises(Exception):
      fight.fightTier
  
  def test_missing_difficulty_fails(self):
    fight = Fight({"lastPhase": 0}, [])
    with pytest.raises(Exception):
      fight.fightTier

class TestCompletionStatus:
  pass

class TestBestParse:
  pass

class TestEmoji:
  pass

class TestColor:
  pass

class TestPartyMembers:
  pass

class TestPartyParses:
  pass

class TestEmbed:
  pass
# If I'm thinking about entry/exit points for Fight:
# test comparison (for each possible if)
# change secondsElapsed/timeElapsed to set variables inside the class
# Test bestParse for a few ranked fights
# Test emojis/colors for a multitude of best parses
# Cursory tests on thumbnail
# Test party members/parses to match website
# To embed works based on certain dummy test data