from sklearn.preprocessing import LabelEncoder


# object인 컬럼만 찾기
# df_final.info()
class Encoder_df:
    def __init__(self, df):
        self.df = df
        self.labelencoder()
        self.label_add_colums()

    def labelencoder(self):
        self.encoder = LabelEncoder()
        self.encoder.fit(list(self.df['Relinquished']))
        self.digit_label_Relinquished = self.encoder.transform(self.df['Relinquished'])

        self.encoder.fit(list(self.df['position']))
        self.digit_label_position = self.encoder.transform(self.df['position'])

    def label_add_colums(self):
        # 새로운 컬럼으로 넣어주기
        self.df['Relinquished_digit'] = self.digit_label_Relinquished
        self.df['position_digit'] = self.digit_label_position
        self.df_new = self.df.drop(['Relinquished', 'position'], axis=1)

    def tensorflow(self):
        self.train_set = self.df_new.sample(frac=.8, random_state=0)
        self.test_set = self.df_new.drop(self.train_set.index)
        return self.train_set, self.test_set