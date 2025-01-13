from enum import IntEnum

class Pull(IntEnum):
  WIPE = 0
  CLEAR = 1
  GRAY = 2
  GREEN = 3
  BLUE = 4
  PURPLE = 5
  ORANGE = 6
  PINK = 7
  GOLD = 8

PULL_HEXCODES = [0xff0000, 0xabebc6, 0x666666, 0x1eff00, 0x0070ff, 
                 0xa335ee, 0xff8000, 0xe268a8, 0xe5cc80]
PULL_EMOJIS = ["❌", "✅", "🩶", "💚", "💙", "💜", "🧡", "🩷", "💛"]

def parseToIndex(parse: int) -> int:
  """
  Takes a parse and outputs an index denoting its percentile range.

  Args:
    `parse` (int): A player's parse on a fight. -1 can be used to indicate a 
    fight that has been cleared but is not ranked.

  Returns:
    int: An index corresponding to the parse. Can be used to access the hexcode
    or emoji corresponding to a cleared fight. An invalid parse returns None.
  """
  # Ranges can be found here: 
  # https://www.archon.gg/ffxiv/articles/help/rankings-and-parses
  if parse == -1: return Pull.CLEAR
  elif parse < 25: return Pull.GRAY
  elif parse < 50: return Pull.GREEN
  elif parse < 75: return Pull.BLUE
  elif parse < 95: return Pull.PURPLE
  elif parse < 99: return Pull.ORANGE
  elif parse == 99: return Pull.PINK
  elif parse == 100: return Pull.GOLD
  else: return None