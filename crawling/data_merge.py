import pandas as pd

nba_retire = pd.read_csv('crawling/player_info.csv')

nba_all = pd.read_csv('crawling/all_seasons.csv')
nba_all.drop('Unnamed: 0', axis=1, inplace=True)


nba_injury = pd.read_csv('crawling/nba_injury_1998.csv')
nba_injury.rename({'Relinquished': 'name'}, axis=1, inplace=True)

# 은퇴  시즌이 2개인 선수들
name_list = nba_retire.groupby(['name']).count().sort_values('age', ascending=False)
name_list = list(name_list[name_list['age'] == 2].index)

# 은퇴 시즌이 2개인 선수들 1개로 만들기
index_list = []
while len(name_list) > 0:
    cnt = len(name_list)
    for idx, value in nba_retire.iterrows():
        if value[0] in name_list:
            index_list.append(idx)
            name_list.remove(value[0])
nba_retire = nba_retire.drop(index_list).reset_index(drop=True)

# 몇 시즌 뛰었는지 계산
nba_player = nba_all.groupby('player_name',
                             as_index=False).agg({'season': 'count'}).sort_values('season',
                                                                                  ascending=False).reset_index(
    drop=True)

# nba은퇴자랑 player 시즌 머지
nba_01 = pd.merge(nba_retire, nba_player, left_on='name', right_on='player_name',
                  how='left').sort_values('season_y').reset_index(drop=True)
nba_01 = nba_01.drop(['season_x', 'player_name'], axis=1).rename({'season_y': 'season'}, axis=1)
# 이름 달라서 그거 바꿔주기
name_list = ['Rasho Nesterovic', 'Zydrunas Ilgauskas', 'Peja Stojakovic', 'T.J. Ford', 'Eduardo Najera',
             'Vladimir Stepania', 'Darko Milicic',
             'Hedo Turkoglu', 'Kosta Perovic', 'Raul Lopez', 'Andres Nocioni', 'Primoz Brezec', 'Bostjan Nachbar',
             'Jiri Welsch',
             'PJ Hairston', 'Manu Ginobili', 'Mike Dunleavy', 'Mirza Teletovic', 'Gerald Henderson', 'Jose Calderon',
             'Kevin Seraphin']
cnt = 0
for i in range(155, 176):
    nba_01.loc[i, 'name'] = name_list[cnt]
    cnt += 1

# nba은퇴자 이름 바꿔서 다시 명단이랑 player 머지
nba_02 = pd.merge(nba_01, nba_player, left_on='name',
                  right_on='player_name').drop(['season_x', 'player_name'], axis=1).rename({'season_y': 'season'},
                                                                                           axis=1)

nba_injury_sum = nba_injury.groupby('name', as_index=False).agg({'Notes': 'count'}).sort_values('Notes',
                                                                                                ascending=False).reset_index(
    drop=True)

# 우선 이름 나누고 다시 for 돌려서 nba_02['name']에 들어있으면 저장
import re

for i in range(nba_injury_sum.shape[0]):
    for namedata in re.split('[/()]', nba_injury_sum.loc[i, 'name']):
        if namedata.strip() in list(nba_02['name']):
            nba_injury_sum.loc[i, 'name'] = namedata.strip()

# Notes에서 NaN값을 발견, dropna함, 최종분석파일
nba_injury_merge = pd.merge(nba_02, nba_injury_sum, on='name', how='left').sort_values('Notes',
                                                                                       ascending=False).reset_index(
    drop=True)
nba_injury_merge.dropna(inplace=True)
nba_injury_merge.sort_values('season', ascending=False).reset_index(drop=True)
nba_injury_merge.to_csv('nba_injury_merge.csv',mode='w',index=False)