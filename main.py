import requests

from bs4 import BeautifulSoup

class SummonerData:
    summoner_name: str
    rank: str
    queue_type: str
    lp: int
    win_rate: int
    games_played: int

    def __init__(self, url):
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, "html.parser")
        #finding summoner name
        self.summoner_name = soup.find('div', class_="summoner-name").text
        champ_list = soup.find('div', class_='champion-list')
        rank_list = soup.find('div', class_='rank-list')
        rank_info = rank_list.find_all('strong')
        self.rank = rank_info[0].text
        self.lp = rank_info[1].text
        self.champName = champ_list.find_all('div', class_='champion-name')
        self.champKD = champ_list.find_all('div', class_='kda-ratio gray-okay-tier')
    def __str__(self):
        return f'''
Summoner Name: {self.summoner_name}
Rank: {self.rank}
LP: {self.lp, "with"}

'''
obj = SummonerData("https://u.gg/lol/profile/na1/ff15open/overview")
print(obj.__str__())
