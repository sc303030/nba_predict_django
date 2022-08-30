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
    injury_df: pd.DataFrame

    def csv_to_list(self, df, columns):
        _data = {i: df[i].values for i in columns}
        return _data

    def merge_position(self):
        df_injury_player_merge = pd.merge(self.player_df, self.merged_df, left_on="Relinquished", right_on="name",
                                          how='right')

    def injury_info_db(self):
        injury_df_drop_notes = self.injury_df.drop('Notes', axis=1)
        merge_df = pd.merge(injury_df_drop_notes, self.player_df, left_on="Relinquished", right_on="name")
        injury_to_list = self.csv_to_list(merge_df, ['Date', 'Team', 'name', 'Notes2'])
        injury_list = []
        for date, team, name, injury_details in zip(injury_to_list['Date'], injury_to_list['Team'],
                                                    injury_to_list['name'], injury_to_list['Notes2']):
            injury_list.append(Injury(date=date, team=team, name=name, injury_details=injury_details))
        Injury.objects.bulk_create(injury_list)

    def player_into_db(self):
        name_list, age_list, year_list = self.csv_to_list()
        players = []
        for name, age, year in zip(name_list, age_list, year_list):
            players.append(Player(name=name, age=age, retire_year=year))
        Player.objects.bulk_create(players)


player_df = pd.read_csv('crawling/player_info.csv')
merged_df = pd.read_csv("crawling/nba_injury_merge_position.csv")
injury_df = pd.read_csv("crawling/nba_injury_1998.csv")
print('Player 시작')
player_info_db = PlayerIntoDb(player_df=player_df, merged_df=merged_df, injury_df=injury_df)
player_info_db.injury_info_db()
# player_info_db.player_into_db()
print('Player 종료')
