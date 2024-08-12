from typing import Any
import discord, sys, os
from discord import app_commands
from discord.ui import Select, View
from discord.ext import commands

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from emoji import emojiDict as emoji

class PreviewSelect(Select):
  def __init__(self) -> None:
    options=[
      discord.SelectOption(
        label="Single Fight", 
        emoji="🔸", 
        description="A single pull."
      ),
      discord.SelectOption(
        label="Multifight", 
        emoji="🔷", 
        description="Multiple pulls of the same encounter."
      ),
      discord.SelectOption(
        label="Compilation", 
        emoji="💠", 
        description="Multiple encounters."
      ),
    ]
    super().__init__(
      placeholder="Select a report type to preview:",
      options=options
    )

  async def callback(self, interaction: discord.Interaction) -> None:
    selection = self.values[0]
    embed = discord.Embed()
    if selection == "Single Fight":
      embed.title = "🔸 Hydaelyn - <t:1720845660:D>"
      embed.url = "https://www.fflogs.com/reports/9mT1qQCXvtFnWpNJ#fight=3"
      embed.set_thumbnail(url="https://assets.rpglogs.com/img/ff/bosses/1059-icon.jpg")
      embed.color = 0xe5cc80
      embed.set_author(name="Uploaded by Eldwin Moonfire")
      embed.add_field(
        name="Status", 
        value="Clear in 8:23", 
        inline=False
      )
      partyMembers = [
        ["Laarion Stormwind", "Paladin", "💜 92"],
        ["Fama Red", "DarkKnight", "💜 82"],
        ["Yunalesca Strife", "WhiteMage", "💙 67"],
        ["Ahrih Valencia", "Scholar", "🩶 3"],
        ["Shalis Addock", "Monk", "💜 77"],
        ["Bruce Elegance", "Samurai", "💜 84"],
        ["Sleepy Eldwin", "Machinist", "💛 100"],
        ["Araiah Scythe", "Summoner", "💚 28"],
      ]
      embed.add_field(
        name="Party", 
        value="\n".join(f"{emoji[member[1]][0]} {member[0]}" 
                        for member in partyMembers), 
        inline=True
      )
      embed.add_field(
        name="Parses", 
        value="\n".join(f"{emoji[member[1]][0]} {member[2]}" 
                        for member in partyMembers), 
        inline=True
      )
    elif selection == "Multifight":
      embed.title = "🔷 Zeromus - <t:1696566152:D>"
      embed.url = "https://www.fflogs.com/reports/rT4xKXkcLgbAqa1d"
      embed.set_thumbnail(url="https://assets.rpglogs.com/img/ff/bosses/1070-icon.jpg")
      embed.color = 0xa335ee #Purple
      embed.set_author(name="Uploaded by dapc")
      embed.add_field(
        name="Pulls", 
        value="18", 
        inline=False
      )
      embed.add_field(
        name="Best Pull", 
        value=f"[Clear in 8:32]({embed.url}#fight=18)", 
        inline=False
      )
      embed.add_field(
        name="Clear Pulls?", 
        value="💜 🧡 🧡 🧡 🧡",
        inline=False
      )
    else:
      embed.title = "Under construction"
    await interaction.response.edit_message(embed=embed, view=None)

class PreviewView(View):
  def __init__(self):
    super().__init__()
    self.add_item(PreviewSelect())

class test(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(
      name = "test",
      description="Testing function"
  )
  async def test(self, interaction: discord.Interaction) -> None:
    view = PreviewView()
    await interaction.response.send_message(view=view)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(test(bot))

#   if message.content == "Test Single":
#     testFieldinLine = {
#        "name": "Sleepy Eldwin",
#        "value": "💛 100 on <:Machinist:1261552059455373392>",
#        "inline": True
#     }
#     testFieldoutLine = {
#       "name": "Sleepy Eldwin",
#       "value": "💛 100 on <:Machinist:1261552059455373392>",
#       "inline": False
#     }
#     singleDict = {
#         "title": "Hydaelyn - <t:1720845660:R>",
#         "url": "https://www.fflogs.com/reports/9mT1qQCXvtFnWpNJ#fight=3",
#         "thumbnail": {
#            "url":"https://assets.rpglogs.com/img/ff/bosses/1059-icon.jpg"
#         },
#         "color": 0xe5cc80,
#         "author": {
#            "name": "Uploaded by Eldwin Moonfire"
#         },
#         "fields": [
#           {
#             "name": "Status",
#             "value": "Clear in 8:23",
#             "inline": False
#           },
#           {
#               "name": "Party Members",
#               "value": "\n".join(list(map(((lambda x: "<:Machinist:1261552059455373392> " + x)), ["Sleepy Eldwin", "Bruce Elegance", "Shalis Addock", "Araiah Scythe", "Laarion Stormwind", "Fama Red", "Yunalesca Strife", "Ahrih Valencia"]))),
#               "inline": True
#           },
#           # ["Sleepy Eldwin", "Bruce Elegance", "Shalis Addock", "Araiah Scythe", "Laarion Stormwind", "Fama Red", "Yunalesca Strife", "Ahrih Valencia"]
#           {
#              "name": "Parses",
#              "value": "\n".join(["<:Machinist:1261552059455373392> 💛 100", "<:Machinist:1261552059455373392> 💛 100", "<:Machinist:1261552059455373392> 💛 100","<:Machinist:1261552059455373392> 💛 100", "<:Machinist:1261552059455373392> 💛 100", "<:Machinist:1261552059455373392> 💛 100", "<:Machinist:1261552059455373392> 💛 100", "<:Machinist:1261552059455373392> 💛 100"]),
#              "inline": True
#           }
#           # {
#           #     "name": "Job",
#           #     "value": "<:Machinist:1261552059455373392>\n<:Samurai:1261552153806241792>\n<:Monk:1261552060193570846>\n<:Summoner:1261552067999305738>\n<:Paladin:1261551950604927107>\n<:DarkKnight:1261551947723440128>\n<:Scholar:1261552002987458630>\n<:WhiteMage:1261552003956346880>",
#           #     "inline": True
#           # },
#           # {
#           #    "name": "Parse",
#           #    "value": "💛 100\n💜 84\n💜 77\n💚 28\n💜 92\n💜 82\n💙 67\n🩶 3",
#           #    "inline": True
#           # }
#         ]
#      }
#     await message.channel.send(embed=discord.Embed.from_dict(singleDict))

#   if message.content == "Test Log Bot":
#       embedVar = discord.Embed(title="The Unending Coil of Bahamut - June 18, 2024",color=0xffd1dc)
#       embedVar.description = "Testing out what a description looks like"
#       embedVar.set_thumbnail(url="https://assets.rpglogs.com/img/ff/bosses/1060-icon.jpg")
#       embedVar.set_author(name="Uploaded by DSXXI")
#       embedVar.add_field(name="Pulls", value="13")
#       # embedVar.add_field(name="Date", value="Today", inline=True)
#       embedVar.add_field(name="Clear?", value="Yes")
#       embedVar.add_field(name="Furthest phase", value="P4")
#       # embedVar.add_field(name="View report", value="[View report](https://www.fflogs.com/reports/7Myb4A6dDq1HnWvc)")
#       embedVar.url = "https://www.fflogs.com/reports/7Myb4A6dDq1HnWvc"
#       # embedVar.add_field(name="Link to report", value="https://www.fflogs.com/reports/7Myb4A6dDq1HnWvc")
      
#       await message.channel.send(embed=embedVar)