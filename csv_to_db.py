import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'nba_predict_django.settings'
import django

django.setup()
from nba_app.models import Player

from dataclasses import dataclass
import pandas as pd


@dataclass
class PlayerIntoDb:
    df: pd.DataFrame

    def csv_to_list(self):
        return self.df['name'].values, self.df['age'].values, self.df['year'].values

    def into_db(self):
        name_list, age_list, year_list = self.csv_to_list()
        players = []
        for name, age, year in zip(name_list, age_list, year_list):
            players.append(Player(name=name, age=age, retire_year=year))
        Player.objects.bulk_create(players)


player_df = pd.read_csv('crawling/player_info.csv')
print('Player 시작')
player_info_db = PlayerIntoDb(player_df)
player_info_db.into_db()
print('Player 종료')
