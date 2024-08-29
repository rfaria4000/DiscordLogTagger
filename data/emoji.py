from typing import NamedTuple, Dict

class JobInfo(NamedTuple):
  emoji: str
  priority:int

emojiDict: Dict[str, JobInfo] = {
  "Paladin": JobInfo("<:Paladin:1261551950604927107>", 0),
  "Warrior": JobInfo("<:Warrior:1261551951255179387>", 1),
  "DarkKnight": JobInfo("<:DarkKnight:1261551947723440128>", 2),
  "Gunbreaker": JobInfo("<:Gunbreaker:1261551948650516482>", 3),

  "WhiteMage": JobInfo("<:WhiteMage:1261552003956346880>", 4),
  "Scholar": JobInfo("<:Scholar:1261552002987458630>", 5),
  "Astrologian": JobInfo("<:Astrologian:1261552000714276864>", 6),
  "Sage": JobInfo("<:Sage:1261552001561530389>", 7),

  "Monk": JobInfo("<:Monk:1261552060193570846>", 8),
  "Dragoon": JobInfo("<:Dragoon:1261552058658455592>", 9),
  "Ninja": JobInfo("<:Ninja:1261552060999143495>", 10),
  "Samurai": JobInfo("<:Samurai:1261552153806241792>", 11),
  "Reaper": JobInfo("<:Reaper:1261552184106160148>", 12),
  "Viper": JobInfo("<:Viper:1261553727463096320>", 13),

  "Bard": JobInfo("<:Bard:1261552055990882376>", 14),
  "Machinist": JobInfo("<:Machinist:1261552059455373392>", 15),
  "Dancer": JobInfo("<:Dancer:1261552057878315088>", 16),

  "BlackMage": JobInfo("<:BlackMage:1261552056804839475>", 17),
  "Summoner": JobInfo("<:Summoner:1261552067999305738>", 18),
  "RedMage": JobInfo("<:RedMage:1261552064614498394>", 19),
  "Pictomancer": JobInfo("<:Pictomancer:1261553983588274206>", 20),
  "BlueMage": JobInfo("<:BlueMage:1261552374296875069>", 21)
}