import requests
import os
import discord

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from discord.ext import commands

class SummonerData:
    summoner_name: str
    rank: str
    queue_type: str
    lp: int
    win_rate: str
    games_played: int
    champName = str
    champKD = int
    champGamesPlayed = int
    champWR = str
    def __init__(self, url):
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, "html.parser")
        #finding summoner name
        self.summoner_name = soup.find('div', class_="summoner-name").text
        #finding rank, lp, winrate
        try:
            rank_list = soup.find('div', class_='rank-list')
            rank_info = rank_list.find_all('strong')
            self.rank = rank_info[0].text
            self.lp = rank_info[1].text
            self.win_rate = soup.find_all('div', class_='rank-wins')
        except:
            self.rank = "No rank"
            self.lp = 0
            self.win_rate = "No rank"
        # top 3 champions
        champ_list = soup.find('div', class_='champion-list')
        self.champName = champ_list.find_all('div', class_='champion-name')
        self.champWR = champ_list.find_all('div', class_='win-rate')
        # self.champGamesPlayed =
    def __str__(self):
        return f'''
        Summoner Name: {self.summoner_name}
        Rank (Solo/Duo): {self.rank} ({self.win_rate[0].text})
        LP: {self.lp}
        Top 5 champions: {self.champName[0].text} with a {self.champWR[0].text} winrate
        '''

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='stats', help ='Says happy birthday to you :)')
async def hbd(ctx, name):
    obj = SummonerData("https://u.gg/lol/profile/na1/" + name + "/overview")
    await ctx.send(obj.__str__())

bot.run(TOKEN)
# name = input("Enter your summoner name:")
# obj = SummonerData("https://u.gg/lol/profile/na1/" + name + "/overview")
# print(obj.__str__())
