import pandas as pd

injury_name_modify_before = ['Radoslav Nesterović', 'Žydrūnas Ilgauskas', 'Peja Stojaković', 'T. J. Ford',
                             'Eduardo Nájera', 'Vladimir Radmanović', 'Darko Miličić', 'Hedo Türkoğlu', 'Kosta Perović',
                             'Raül López', 'Andrés Nocioni', 'Primož Brezec', 'Boštjan Nacchbar', 'Jiří Welsch',
                             'P.J.Hairston', 'Manu Ginóbili', 'Mike Dunleavy Jr.', 'Mirza Teletović',
                             'Gerald Henderson Jr.', 'José Calderón', 'Kevin Séraphin']

injury_df = pd.read_csv('crawling/nba_injury_1998.csv')
merged_position = pd.read_csv('crawling/nba_injury_merge_position.csv')

name_1 = injury_df['Relinquished']
name_2 = merged_position['name']
dfdf = injury_df.groupby(['Relinquished'])
