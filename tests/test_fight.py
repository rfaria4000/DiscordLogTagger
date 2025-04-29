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

  def test_init_succeeds_with_valid_data(self, grab_extreme_fight):
    fight_data, actor_data, ranking_data = grab_extreme_fight(9, 0)
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
  def mock_parse_dependencies(self):
    def mock_property(prop):
      return property(lambda self: self.fightData[prop],
                      lambda self, value: None)
    
    with (
      patch.object(Fight, "fightTier", mock_property("fightTier")),
      patch.object(Fight, "timeElapsed", mock_property("timeElapsed")),
      patch.object(Fight, "bestParse", mock_property("bestParse"))
    ):
      yield 

  def test_assignment(self):
    fight = Fight({"fightTier": 3, "timeElapsed": 900}, [])
    assert fight.fightTier == 3
    assert fight.timeElapsed == 900

  def test_comparison_to_non_fight(self, empty_fight):
    assert empty_fight != ""

  def test_fight_tier(self):
    fight1 = Fight({"fightTier": 3}, [])
    fight2 = Fight({"fightTier": 2}, [])
    assert fight1 > fight2
  
  def test_kill_status(self):
    fight1 = Fight({"fightTier": 2, "kill": True}, [])
    fight2 = Fight({"fightTier": 2, "kill": False}, [])
    assert fight1 > fight2

  def test_encounter_id(self):
    fight1 = Fight({"fightTier": 2, "kill": True, "encounterID": 2}, [])
    fight2 = Fight({"fightTier": 2, "kill": True, "encounterID": 1}, [])
    assert fight1 > fight2

  def test_fight_percentage(self):
    fight1 = Fight({
      "fightTier": 2, 
      "kill": True, 
      "encounterID": 1, 
      "fightPercentage": 50
      }, [])
    fight2 = Fight({
      "fightTier": 2, 
      "kill": True, 
      "encounterID": 1, 
      "fightPercentage": 100
      },[])
    assert fight1 > fight2

  def test_best_parse(self):
    fight1 = Fight({
      "fightTier": 2, 
      "kill": True, 
      "encounterID": 1, 
      "fightPercentage": 50,
      "bestParse": 99
      }, [], {"name": "Neri"})
    fight2 = Fight({
      "fightTier": 2, 
      "kill": True, 
      "encounterID": 1, 
      "fightPercentage": 50,
      "bestParse": 80
      }, [], {"name": "Neri"})
    assert fight1 > fight2

  def test_shortest_fight(self):
    fight1 = Fight({
      "fightTier": 2, 
      "kill": True, 
      "encounterID": 1, 
      "fightPercentage": 50,
      "timeElapsed": 100
      }, [])
    fight2 = Fight({
      "fightTier": 2, 
      "kill": True, 
      "encounterID": 1, 
      "fightPercentage": 50,
      "timeElapsed": 120
      }, [])
    assert fight1 > fight2

  def test_fails_without_sufficient_properties(self):
    fight1 = Fight({"fightTier": 2}, [])
    fight2 = Fight({"fightTier": 2}, [])
    with pytest.raises(Exception):
      fight1 > fight2
  
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
  @pytest.fixture(autouse=True)
  def mock_parse_dependencies(self):
    def mock_property(prop):
      return property(lambda self: self.fightData[prop],
                      lambda self, value: None)
    with (
      patch.object(Fight, 
                   "timeElapsed", 
                   new_callable=PropertyMock) as mock_time, 
      patch.object(Fight,
                   "fightTier",
                   mock_property("fightTier")) as mock_tier,
    ):
      mock_time.return_value = "10:10"
      yield mock_time, mock_tier
   
  @pytest.fixture(autouse=True)
  def mock_stubs(self):
    with patch("fight.FightTier") as mock_reference_tiers:
      mock_reference_tiers.ULTIMATE = "Ultimate"
      yield mock_reference_tiers

  def test_clear_status(self):
    fight = Fight({"kill": True, "timeElapsed": None}, [])
    assert fight.completionStatus == "Clear in 10:10"

  def test_fails_without_kill_status(self, empty_fight):
    with pytest.raises(Exception):
      empty_fight.completionStatus

  def test_ultimate_fails_without_last_phase(self):
    fight = Fight({"kill": False, 
                   "fightTier": "Ultimate", 
                   "bossPercentage": 50}, [])
    with pytest.raises(Exception):
      fight.completionStatus

  def test_ultimate_fails_without_boss_percentage(self):
    fight = Fight({"kill": False, 
            "fightTier": "Ultimate", 
            "lastPhase": 3
            }, [])
    with pytest.raises(Exception):
      fight.completionStatus

  def test_ultimate_status(self):
    fight = Fight({"kill": False, 
            "fightTier": "Ultimate", 
            "bossPercentage": 50,
            "lastPhase": 3
            }, [])
    assert fight.completionStatus == f"Phase 3 - 50% remaining"

  def test_non_ultimate_status(self):
    fight = Fight({"kill": False, 
        "fightTier": "Savage", 
        "bossPercentage": 50,
        "lastPhase": 0
        }, [])
    assert fight.completionStatus == f"50% remaining"
  
  def test_non_ultimate_fails_without_boss_percentage(self):
    fight = Fight({"kill": False, 
            "fightTier": "Savage", 
            "lastPhase": 3
            }, [])
    with pytest.raises(Exception):
      fight.completionStatus

class TestBestParse:
  def test_fails_without_kill(self):
    fight = Fight({"id": 1}, [], {})
    with pytest.raises(Exception):
      fight.bestParse
  
  def test_no_clear_parse(self):
    fight = Fight({"kill": False}, [])
    assert fight.bestParse == -1

  def test_no_ranking_parse(self):
    fight = Fight({"kill": True}, [])
    assert fight.bestParse == -1

  #TODO: Empty friendly players should handle gracefully
  def test_grabs_best_parse(self):
    fight = Fight({"kill": True}, [], {"name": "Neri"})
    assert fight.bestParse == -1

  # --- Integration Tests ---

  def test_ranking_and_clear_parse(self,
                                   sample_fight_data, 
                                   sample_actor_data, 
                                   sample_ranking_data):
    fight = Fight(sample_fight_data, sample_actor_data, sample_ranking_data)
    assert fight.bestParse == 99

  def test_sample_extreme(self, grab_extreme_fight):
    fight_data, actor_data, ranking_data = grab_extreme_fight(9, 0)
    fight = Fight(fight_data, actor_data, ranking_data)
    assert fight.bestParse == 79

# ---

@pytest.fixture
def mock_parse_dependencies():
  with (
    patch.object(Fight, 
                  "bestParse", 
                  new_callable=PropertyMock) as mock_best_parse,
    patch("fight.parses") as mock_parses
  ):
    yield mock_best_parse, mock_parses

class TestEmoji:
  def test_fails_on_empty(self, empty_fight):
    with pytest.raises(Exception):
      empty_fight.emoji

  def test_no_clear_emoji(self, mock_parse_dependencies):
    fight = Fight({"kill": False}, [])
    
    _, mock_parses = mock_parse_dependencies
    mock_parses.Pull.WIPE = 0
    mock_parses.PULL_EMOJIS = ["🚫"]

    assert fight.emoji == "🚫"

  def test_clear_emoji(self, mock_parse_dependencies):
    fight = Fight({"kill": True}, [])

    mock_best_parse, mock_parses = mock_parse_dependencies
    mock_best_parse.return_value = 90
    mock_parses.parseToIndex.return_value = 0
    mock_parses.PULL_EMOJIS = ["🏆"]
    
    assert fight.emoji == "🏆"

class TestColor:
  pass

class TestDisplayPartyMembers:
  pass

class TestDisplayPartyParses:
  pass

class TestEmbed:
  pass

# If I'm thinking about entry/exit points for Fight:
# Test bestParse for a few ranked fights
# Test emojis/colors for a multitude of best parses
# Cursory tests on thumbnail
# Test party members/parses to match website
# To embed works based on certain dummy test data