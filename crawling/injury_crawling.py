import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
service = ChromeService(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)


def craw(start, end):
    page_list = [i for i in range(start, end, 25)]
    Date = []
    Team = []
    Acquired = []
    Relinquished = []
    Notes = []
    for page in page_list:
        driver.get(
            'http://www.prosportstransactions.com/basketball/Search/SearchResults.php?Player=&Team=&BeginDate=1998-01-01&EndDate=2020-12-31&ILChkBx=yes&Submit=Search&start=' + str(
                page))
        page = driver.find_elements(By.CSS_SELECTOR, '.datatable')
        if len(page) != 0:
            for i in page[0].find_elements(By.TAG_NAME, 'tbody'):
                k = i.find_elements(By.TAG_NAME, 'tr')
                for data in k:
                    ll = data.find_elements(By.TAG_NAME, 'td')
                    Date.append(ll[0].text)
                    Team.append(ll[1].text)
                    Acquired.append(ll[2].text)
                    Relinquished.append(ll[3].text)
                    Notes.append(ll[4].text)
    return Date, Team, Acquired, Relinquished, Notes


Date, Team, Acquired, Relinquished, Notes = craw(0, 5001)
Date1, Team1, Acquired1, Relinquished1, Notes1 = craw(5001, 10001)
Date2, Team2, Acquired2, Relinquished2, Notes2 = craw(10001, 15001)
Date3, Team3, Acquired3, Relinquished3, Notes3 = craw(15000, 20001)
Date4, Team4, Acquired4, Relinquished4, Notes4 = craw(20001, 25001)
Date5, Team5, Acquired5, Relinquished5, Notes5 = craw(25001, 28526)

data_collection = [[Date, Team, Acquired, Relinquished, Notes],
                   [Date1, Team1, Acquired1, Relinquished1, Notes1],
                   [Date2, Team2, Acquired2, Relinquished2, Notes2],
                   [Date3, Team3, Acquired3, Relinquished3, Notes3],
                   [Date4, Team4, Acquired4, Relinquished4, Notes4],
                   [Date5, Team5, Acquired5, Relinquished5, Notes5]]


def create_dataframe(date, team, acquired, relinquished, notes):
    df = pd.DataFrame({
        'Date': date,
        'Team': team,
        'Acquired': acquired,
        'Relinquished': relinquished,
        'Notes': notes
    })
    return df


data_df = {}

for idx, datas in enumerate(data_collection):
    date, team, acquired, relinquished, notes = datas
    data_df[f"df{idx}"] = create_dataframe(Date, Team, Acquired, Relinquished, Notes)

nba_injury_1998 = pd.concat([*data_df.values()])
drop_index = list(nba_injury_1998[nba_injury_1998['Date'] == ' Date'].index)
nba_injury_1998 = nba_injury_1998.drop(drop_index).reset_index(drop=True)
none_Relinquished = list(nba_injury_1998[nba_injury_1998['Relinquished'] == ''].index)
nba_injury_1998 = nba_injury_1998.drop(none_Relinquished).reset_index(drop=True)
nba_injury_1998 = nba_injury_1998.drop(['Acquired'], axis=1)
nba_injury_1998.to_csv('nba_injury_1998.csv', mode='w', index=False)

for i in range(nba_injury_1998.shape[0]):
    if nba_injury_1998.loc[i, 'Relinquished'] != '':
        nba_injury_1998.loc[i, 'Relinquished'] = nba_injury_1998.loc[i, 'Relinquished'].split('•')[1].strip()
        nba_injury_1998.loc[i, 'Date'] = nba_injury_1998.loc[i, 'Date'].strip()
        nba_injury_1998.loc[i, 'Team'] = nba_injury_1998.loc[i, 'Team'].strip()
        nba_injury_1998.loc[i, 'Notes'] = nba_injury_1998.loc[i, 'Notes'].strip()
    if nba_injury_1998.loc[i, 'Relinquished'] == '':
        nba_injury_1998.loc[i, 'Relinquished'] = nba_injury_1998.loc[i, 'Relinquished']
        nba_injury_1998.loc[i, 'Date'] = nba_injury_1998.loc[i, 'Date'].strip()
        nba_injury_1998.loc[i, 'Team'] = nba_injury_1998.loc[i, 'Team'].strip()
        nba_injury_1998.loc[i, 'Notes'] = nba_injury_1998.loc[i, 'Notes'].strip()

for i in range(nba_injury_1998.shape[0]):
    data = nba_injury_1998.loc[i, 'Notes'].split('with')
    if data[0] in ['placed on IL ', 'placed on IR ']:
        nba_injury_1998.loc[i, 'Notes2'] = data[1].strip()
    else:
        nba_injury_1998.loc[i, 'Notes2'] = nba_injury_1998.loc[i, 'Notes']

nba_injury_1998.to_csv('crawling/nba_injury_1998.csv', mode='w', index=False)
