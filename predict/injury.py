import pandas as pd


class injury:
    def __init__(self, acl_achilles_df, injury_df, nba_all_df):
        self.acl_achilles_df = acl_achilles_df
        self.injury_df = injury_df
        self.nba_all_df = nba_all_df
        self.merge()
        self.age_func()

    def merge(self):
        self.df_merge1 = pd.merge(self.acl_achilles_df, self.injury_df, left_on='Relinquished', right_on='name').drop(
            'name', axis=1)

    def age_func(self):
        # 평균을 구하고 모두 소수 2번쨰까지만 살리기
        self.nba_all_group = self.nba_all_df.groupby('player_name', as_index=False).mean()
        for i in range(self.nba_all_group.shape[0]):
            for i2 in range(len(list(self.nba_all_group.columns))):
                if i2 == 0:
                    continue
                elif i2 == 1:
                    self.nba_all_group.iloc[i, i2] = self.nba_all_group.iloc[i, i2].astype('int64')
                else:
                    self.nba_all_group.iloc[i, i2] = round(self.nba_all_group.iloc[i, i2], 2)

        self.nba_all_group['age'] = self.nba_all_group['age'].astype('int64')

    def final_df(self):
        self.df_merge_final = pd.merge(self.df_merge1, self.nba_all_group, left_on='Relinquished',
                                       right_on='player_name', how='left'). \
            drop('age_y', axis=1).rename(columns={'age_x': 'age'})

        self.df_merge_final.drop('player_name', axis=1, inplace=True)

        self.df_merge_final['Notes'] = self.df_merge_final['Notes'].astype(int)
        self.df_merge_final.head()
        return self.df_merge_final
