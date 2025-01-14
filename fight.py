import functools

@functools.total_ordering
class Fight:
  """
  Represents a fight, or a more commonly known as a pull of a duty.
  """
  def __init__(self, fightData, actorData, rankingData = None):
    self.fightData = fightData
    self.actorData = actorData
    self.rankingData = rankingData

  def unpack_data(self):
    pass

  # For debugging purposes?
  def __str__(self):
    pass

  def __eq__(self, other):
    pass

  # for fights within the same category of ult/savage etc, it seems
  # bigger number for encounterID is more recent
  def __gt__(self, other):
    pass



  # I'm going to need a fight to embed function
  # a comparison function for ordering purposes
