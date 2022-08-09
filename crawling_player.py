from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'nba_predict_django.settings'
import django

django.setup()
from nba_app.models import Player

from dataclasses import dataclass
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
service = ChromeService(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)


def craw():
    time_list = ['2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19',
                 '2019-20', '2020-21']
    day_list = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
    name_list = []
    age_list = []
    year_list = []
    cnt = 0
    for day in time_list:
        driver.get('https://en.wikipedia.org/wiki/List_of_' + str(day) + '_NBA_season_transactions')
        page = driver.find_elements(By.CSS_SELECTOR, '.wikitable')
        print(page[0])
        page = page[0]
        for i in page.find_elements(By.TAG_NAME, 'tbody'):
            k = i.find_elements(By.TAG_NAME, 'tr')
            for idx, j in enumerate(k):
                if idx == 0:
                    continue
                else:
                    td_list = j.find_elements(By.TAG_NAME, 'td')
                    if len(td_list) == 6:
                        name_list.append(j.find_elements(By.TAG_NAME, 'td')[1].text)
                        age_list.append(j.find_elements(By.TAG_NAME, 'td')[3].text)
                        year_list.append(day_list[cnt])
                    elif len(td_list) == 5:
                        name_list.append(j.find_elements(By.TAG_NAME, 'td')[0].text)
                        age_list.append(j.find_elements(By.TAG_NAME, 'td')[2].text)
                        year_list.append(day_list[cnt])
            cnt += 1
            print(cnt)
    return name_list, age_list, year_list


name_list, age_list, year_list = craw()


@dataclass
class PlayerIntoDb:
    name_list: list
    age_list: list
    year_list: list

    def into_db(self):
        players = []
        for name, age, year in zip(self.name_list, self.age_list, self.year_list):
            players.append(Player(name=name, age=age, retire_year=year))
        Player.objects.bulk_create(players)


print('Player 시작')
player_info_db = PlayerIntoDb(name_list, age_list, year_list)
player_info_db.into_db()
print('Player 종료')
