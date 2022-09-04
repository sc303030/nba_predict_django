import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'nba_predict_django.settings'
import django

django.setup()
from nba_app.models import Player, Injury

from dataclasses import dataclass
import pandas as pd


@dataclass(init=True)
class PlayerIntoDb:
    player_df: pd.DataFrame
    position_df: pd.DataFrame
    injury_df: pd.DataFrame
    player_position_df: pd.DataFrame = pd.DataFrame({})

    def __init__(self, _player_df, _position_df, _injury_df):
        merge_player_info_position = _player_df.merge(_position_df, on='name')
        merge_player_info_position.drop('age_x', axis=1, inplace=True)
        merge_player_info_position.rename(columns={"age_y": "age"}, inplace=True)
        merge_player_info_position = merge_player_info_position.astype({"Notes": 'int64'})
        self.player_df = _player_df
        self.position_df = _position_df
        self.injury_df = _injury_df
        self.player_position_df = merge_player_info_position

    @classmethod
    def csv_to_list(cls, df, columns):
        _data = [df[i].values for i in columns]
        return _data

    def merge_position(self):
        df_injury_player_merge = pd.merge(self.player_df, self.merged_df, left_on="Relinquished", right_on="name",
                                          how='right')
        print(df_injury_player_merge)

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
        player_info_list = self.csv_to_list(self.player_position_df, self.player_position_df.columns)
        players = []
        for name, year, age, season, notes, position in zip(*player_info_list):
            players.append(
                Player(name=name, age=age, retire_year=year, season=season, injury_count=notes, position=position))
        Player.objects.bulk_create(players)


player_df = pd.read_csv('crawling/player_info.csv')
merged_df = pd.read_csv("crawling/nba_injury_merge_position.csv")
injury_df = pd.read_csv("crawling/nba_injury_1998.csv")
print('Player 시작')
player_info_db = PlayerIntoDb(player_df, merged_df, injury_df)
# player_info_db.injury_info_db()
# player_info_db.merge_position()
player_info_db.player_into_db()
print('Player 종료')
