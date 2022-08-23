import pnadas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
options = webdriver.ChromeOptions()
service = ChromeService(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

position_name = list(nba_injury_merge['name'])
position_name

position_dic = {}
for name in position_name:
    position_dic[name] = 0
position_dic

driver.get('https://www.nba.com/players')
page = driver.find_elements_by_css_selector('.Toggle_slider__hCMQQ')[0].click()
key_words = driver.find_elements_by_css_selector('.Input_input__3YQfM')[0]
for names in list(position_dic.keys()):
    try:
        key_words.send_keys(names)
        time.sleep(1)
        position_table = driver.find_elements_by_css_selector('.players-list')[0]
        position_tr = position_table.find_elements_by_tag_name('tr')[1]
        position_td = position_tr.find_elements_by_tag_name('td')[3].text
        position_dic[names] = position_td
        print(position_td)
        key_words.clear()
        time.sleep(1)
    except:
        position_dic[names] = 0

#     name_word = 'Manu Ginobili'
#     key_words.send_keys(name_word)


for key, value in position_dic.items():
    if value == 0:
        print(key)

def posi(x,position_dic):
    posi = ''
    for key, value in position_dic.items():
        if x == key:
            return value

nba_injury_merge['position'] = nba_injury_merge['name'].apply(lambda x:posi(x,position_dic))
nba_injury_merge

nba_injury_merge.to_csv('nba_injury_merge_position.csv',mode='w',index=False)