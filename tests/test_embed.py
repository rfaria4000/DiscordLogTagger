import os, json
import embed
import pytest

@pytest.mark.parametrize("blank", (None, None))
class TestEmbed:  
  @pytest.fixture(scope="function", autouse=True)
  def setup_and_teardown(self, blank):
    print("setup")
    yield
    print("teardown")

  #TODO: Extract methods from test_embed_compilation
  def test_embed_author(self, blank):
    print("inside test")
    # assert()
  
  # def test_embed_link(self):
  #   assert()

  # def test_embed_time(self):
  #   assert()

  