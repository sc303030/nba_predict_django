from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import pandas as pd

options = webdriver.ChromeOptions()
service = ChromeService(executable_path='crawling/chromedriver.exe')
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
    return name_list, age_list, year_list


name_list, age_list, year_list = craw()
player_df = pd.DataFrame({'name': name_list, 'age': age_list, 'year': year_list})
player_df.to_csv('crawling/player_info.csv', index=False)
