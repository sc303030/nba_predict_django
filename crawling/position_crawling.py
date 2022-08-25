import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = ChromeService(executable_path='crawling/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)


def get_injury_name_dict():
    nba_injury_merge = pd.read_csv("crawling/nba_injury_merge.csv")
    position_name = list(nba_injury_merge['name'])

    position_dic = {}
    for name in position_name:
        position_dic[name] = 0
    return nba_injury_merge, position_dic


def crawling_position(position_dic):
    driver.get('https://www.nba.com/players')
    driver.find_elements(By.CSS_SELECTOR, '.Toggle_slider__hCMQQ')[0].click()
    key_words = driver.find_elements(By.CSS_SELECTOR, '.Input_input__3YQfM')[0]
    for names in list(position_dic.keys()):
        try:
            key_words.send_keys(names)
            time.sleep(1)
            position_table = driver.find_elements(By.CSS_SELECTOR, '.players-list')[0]
            position_tr = position_table.find_elements(By.TAG_NAME, 'tr')[1]
            position_td = position_tr.find_elements(By.TAG_NAME, 'td')[3].text
            position_dic[names] = position_td
            key_words.clear()
            time.sleep(1)
        except:
            position_dic[names] = 0
    return position_dic


def posi(x, position_dic):
    for key, value in position_dic.items():
        if x == key:
            return value


def write_to_dir(nba_injury_merge, position_dic):
    nba_injury_merge['position'] = nba_injury_merge['name'].apply(lambda x: posi(x, position_dic))
    nba_injury_merge.to_csv('crawling/nba_injury_merge_position.csv', mode='w', index=False)


def make_dataframe():
    nba_injury_merge, position_dic = get_injury_name_dict()
    position_dic = crawling_position(position_dic)
    print(position_dic)
    write_to_dir(nba_injury_merge, position_dic)


if __name__ == "__main__":
    make_dataframe()
