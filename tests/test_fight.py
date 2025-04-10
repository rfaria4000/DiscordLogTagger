import pytest
from fight import Fight

class TestInit():
  def test_init_succeeds_with_placeholders(self):
    fight = Fight({}, [])
    assert(True)

  def test_init_sets_fight_data(self):
    pass
  
  def test_init_sets_actor_data(self):
    pass

  def test_init_sets_ranking_data_when_missing(self):
    pass

  def test_init_sets_ranking_data_when_given(self):
    pass

  def test_init_succeeds_with_valid_data(self):
    pass

  def test_fails_without_arguments(self):
    with pytest.raises(Exception):
      fight = Fight()

  def test_inherits_fields_from_fight_data(self):
    pass



# If I'm thinking about entry/exit points for Fight:
# test exit point for each variable
# test setting attributes from fightData
# test unpack party members
# test comparison (for each possible if)
# change secondsElapsed/timeElapsed to set variables inside the class
# Test bestParse for a few ranked fights
# Test emojis/colors for a multitude of best parses
# Cursory tests on thumbnail
# Test party members/parses to match website
# To embed works based on certain dummy test data