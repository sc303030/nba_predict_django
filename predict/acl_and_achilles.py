import re
import pandas as pd


class AclAndAchilles:
    def __init__(self, df):
        self.df = df
        self.yes_no_df()
        self.seasonout_df()
        self.yes_no2_df()
        self.one_or_zero_df()

    # 우선은 ACL과 아킬레스가 들어간  선수 구분
    @staticmethod
    def yes_no(x):
        words = x.split(' ')
        #         print(words)
        for word in words:
            if word.upper() in ['ACL', 'PCL', 'ACHILLES']:
                return True
                break

    def yes_no_df(self):
        self.df['tf'] = self.df['Notes2'].apply(lambda x: self.yes_no(x))

    # 시즌아웃 부상
    @staticmethod
    def seasonout(x):
        words = re.split('\(|\)', x)
        #         print(words)
        for word in words:
            if word in ['out for season']:
                return True
                break

    def seasonout_df(self):
        self.df['out'] = self.df['Notes2'].apply(lambda x: self.seasonout(x))

    # 횟수 카운트
    @staticmethod
    def yes_no2(x):
        words = x.split(' ')
        #         print(words)
        sum_sum = 0
        for word in words:
            if word.upper() in ['ACL', 'PCL', 'ACHILLES'] or word.upper() in ['TORN', 'RUPTURE']:
                sum_sum += 1
            if sum_sum >= 2:
                return True
                break

    def yes_no2_df(self):
        self.df['tf2'] = self.df['Notes2'].apply(lambda x: self.yes_no2(x))

    # 아킬레스와 십자인대 부상 전적 여부
    @staticmethod
    def one_or_zero(x):
        two = 0
        three = 0
        if x['out'] == True:
            two = 1
        if x['tf2'] == True:
            three = 1
        #         print(two, three)
        return pd.Series([two, three])

    def one_or_zero_df(self):
        self.df[['outnum', 'tf2num']] = self.df[['out', 'tf2']].apply(self.one_or_zero, axis=1)

    def df1(self):
        return self.df.groupby('Relinquished', as_index=False).agg({'outnum': 'sum', 'tf2num': 'sum'})
