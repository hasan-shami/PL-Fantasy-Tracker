import pandas as pd
from selenium import webdriver
import datetime
import time
from selenium.common.exceptions import NoSuchElementException

path = r'C:\Users\Hasan\chromedriver_win32\chromedriver.exe'
# Press the green button in the gutter to run the script.
driver = webdriver.Chrome(executable_path=path)
driver.get('https://fantasy.premierleague.com/statistics')


# Check for "Accept cookies" message
time.sleep(10)
try:
    driver.find_element_by_xpath('//button[contains(@class,"accept-all")]').click()
except NoSuchElementException:
    driver.implicitly_wait(10)
    print("not found")


players = driver.find_element_by_xpath('//table[contains(@class,"Table")]//tbody')
flag = "View player information\n"
players_list=players.text.split(flag)
players_list.pop(0)
next_button = driver.find_element_by_xpath('//div[@class="sc-bdnxRM sc-gtsrHT eVZJvz gfuSqG"]//button[3]')

# Extract players list
for x in range(0,20):
    next_button.click()
    players = driver.find_element_by_xpath('//table[contains(@class,"Table")]//tbody')
    players_temp_list = players.text.split(flag)
    players_temp_list.pop(0)
    players_list = players_list + players_temp_list

# Formatting players
players_list = [player.split('\n') for player in players_list]
for player in players_list:
    if len(player)==5:
        del(player[4])
    elif len(player)==4:
        del(player[3])
    player[2]= player[2].split(' ')
    player.append(player[1][0:3])
    player[1]=player[1][3:6]
    if len(player)==5:
        player[3], player[4] = player[4], player[3]


# DataFrame operations
df = pd.DataFrame(players_list, columns=['Name','Position','Stats','Team', 'Playing Chance'])
df['Cost']=df['Stats'].str[0].apply(pd.to_numeric)
df['Selected By %']=df['Stats'].str[1]
df['Selected By %']=df['Selected By %'].apply(lambda x: x.rstrip('%')).apply(pd.to_numeric)
df['Form']=df['Stats'].str[2].apply(pd.to_numeric)
df['Points']=df['Stats'].str[3].apply(pd.to_numeric)
df.drop(columns='Stats', inplace=True)
df['Key']=df['Name']+"/"+df["Position"]+"/"+df["Team"]
df['Date']=datetime.datetime.now()
#.strftime("%Y-%m-%d %H:%M:%S")
# Join function with existing data
master_df = pd.read_excel("FPL_Master.xlsx")
master_df = master_df.append(df)
master_df.to_excel("FPL_Master.xlsx", index=False)



