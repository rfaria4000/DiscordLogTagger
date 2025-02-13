import discord, sys, os
from discord import app_commands
from discord.ui import Select, View
from discord.ext import commands
from typing import NamedTuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import data.jobinfo as jobs

class PartyMember(NamedTuple):
  name: str
  job: str
  parse: str

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
      embed.set_thumbnail(
        url="https://assets.rpglogs.com/img/ff/bosses/1059-icon.jpg",
      )
      embed.color = 0xe5cc80
      embed.set_author(
        name="Uploaded by Eldwin Moonfire",
      )
      embed.add_field(
        name="Status", 
        value="Clear in 8:23", 
        inline=False
      )
      partyMembers = [
        PartyMember("Laarion Stormwind", "Paladin", "💜 92"),
        PartyMember("Fama Red", "DarkKnight", "💜 82"),
        PartyMember("Yunalesca Strife", "WhiteMage", "💙 67"),
        PartyMember("Ahrih Valencia", "Scholar", "🩶 3"),
        PartyMember("Shalis Addock", "Monk", "💜 77"),
        PartyMember("Bruce Elegance", "Samurai", "💜 84"),
        PartyMember("Sleepy Eldwin", "Machinist", "💛 100"),
        PartyMember("Araiah Scythe", "Summoner", "💚 28"),
      ]
      embed.add_field(
        name="Party", 
        value="\n".join(f"{jobs.emojiDict[member.job].emoji} {member.name}" 
                        for member in partyMembers), 
        inline=True
      )
      embed.add_field(
        name="Parses", 
        value="\n".join(f"{jobs.emojiDict[member.job].emoji} {member.parse}" 
                        for member in partyMembers), 
        inline=True
      )
    elif selection == "Multifight":
      embed.title = "🔷 Zeromus - <t:1696566152:D>"
      embed.url = "https://www.fflogs.com/reports/rT4xKXkcLgbAqa1d"
      embed.set_thumbnail(
        url="https://assets.rpglogs.com/img/ff/bosses/1070-icon.jpg",
      )
      embed.color = 0xff8000 #Orange
      embed.set_author(
        name="Uploaded by dapc",
      )
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
      embed.title = "💠 Multiple Fights - <t:1716689181:D>"
      embed.url = "https://www.fflogs.com/reports/CRh38LcT7BzAdHyr"
      embed.set_thumbnail(
        url="https://assets.rpglogs.com/img/ff/bosses/1065-icon.jpg",
      )
      embed.color = 0x0070ff #Blue
      embed.set_author(
        name="Uploaded by DSXXI",
      )
      embed.add_field(
        name="Notable Fights",
        value="Dragonsong's Reprise",
        inline=False
      )
      embed.add_field(
        name="Fight",
        value="Dragonsong's Reprise",
        inline=True
      )
      embed.add_field(
        name="Pulls",
        value="22",
        inline=True
      )
      embed.add_field(
        name="Clears?",
        value="💙",
        inline=True
      )
    
    await interaction.response.edit_message(
      embed=embed, 
      view=None,
    )

class PreviewView(View):
  def __init__(self):
    super().__init__()
    self.add_item(PreviewSelect())

class preview(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(
      name = "preview",
      description="Preview a certain kind of report."
  )
  async def preview(self, interaction: discord.Interaction) -> None:
    view = PreviewView()
    await interaction.response.send_message(view=view)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(preview(bot))