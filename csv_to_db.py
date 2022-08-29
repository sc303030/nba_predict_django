import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'nba_predict_django.settings'
import django

django.setup()
from nba_app.models import Player, Injury

from dataclasses import dataclass
import pandas as pd


@dataclass
class PlayerIntoDb:
    player_df: pd.DataFrame
    merged_df: pd.DataFrame

    def csv_to_list(self):
        return self.player_df['name'].values, self.player_df['age'].values, self.player_df['year'].values

    def merge_position(self):
        _notes_drop = self.player_df.drop(['Notes'], axis=1, inplace=True)
        df_injury_player_merge = pd.merge(_notes_drop, self.merged_df, left_on="Relinquished", right_on="name",
                                          how='right')

    def injury_info_db(self):
        pass

    def player_into_db(self):
        name_list, age_list, year_list = self.csv_to_list()
        players = []
        for name, age, year in zip(name_list, age_list, year_list):
            players.append(Player(name=name, age=age, retire_year=year))
        Player.objects.bulk_create(players)


player_df = pd.read_csv('crawling/player_info.csv')
merged_df = pd.read_csv("crawling/nba_injury_merge_position.csv")

print('Player 시작')
player_info_db = PlayerIntoDb(player_df=player_df, merged_df=merged_df)
player_info_db.player_into_db()
print('Player 종료')
