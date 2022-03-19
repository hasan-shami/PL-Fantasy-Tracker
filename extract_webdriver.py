import pandas as pd
from selenium import webdriver
import datetime
import time
from selenium.common.exceptions import NoSuchElementException

# Initialize. When adding merged_df functionalities, put this function in another py file
def initialize_driver():
    path = r'C:\Users\Hasan\chromedriver_win32\chromedriver.exe'  # Context for OS
    driver = webdriver.Chrome(executable_path=path)
    driver.get('https://fantasy.premierleague.com/statistics')

    # Check for "Accept cookies" message
    time.sleep(5)
    try:
        driver.find_element_by_xpath('//button[contains(@class,"accept-all")]').click()
    except NoSuchElementException:
        driver.implicitly_wait(10)
        print("not found")
    return driver


def get_player_standard(driver):
    # Get players info on page
    players = driver.find_element_by_xpath('//table[contains(@class,"Table")]//tbody')
    flag = "View player information\n"
    players_list = players.text.split(flag)
    players_list.pop(0)
    next_button = driver.find_element_by_xpath('//div[@class="sc-bdnxRM sc-gtsrHT eVZJvz gfuSqG"]//button[3]')

    # Extract players list
    while next_button.is_enabled():
        next_button.click()
        players = driver.find_element_by_xpath('//table[contains(@class,"Table")]//tbody')
        players_temp_list = players.text.split(flag)
        players_temp_list.pop(0)
        players_list = players_list + players_temp_list
    return players_list


def format_players(players_list):
    # Formatting players
    players_list = [player.split('\n') for player in players_list]
    for player in players_list:
        if len(player) == 5:
            del (player[4])
        elif len(player) == 4:
            del (player[3])
        player[2] = player[2].split(' ')
        player.append(player[1][0:3])
        player[1] = player[1][3:6]
        if len(player) == 5:
            player[3], player[4] = player[4], player[3]

    # DataFrame operations
    df = pd.DataFrame(players_list, columns=['Name', 'Position', 'Stats', 'Team', 'Playing Chance'])
    df['Cost'] = df['Stats'].str[0].apply(pd.to_numeric)
    df['Selected By %'] = df['Stats'].str[1]
    df['Selected By %'] = df['Selected By %'].apply(lambda x: x.rstrip('%')).apply(pd.to_numeric)
    df['Form'] = df['Stats'].str[2].apply(pd.to_numeric)
    df['Points'] = df['Stats'].str[3].apply(pd.to_numeric)
    df.drop(columns='Stats', inplace=True)
    df['Key'] = df['Name'] + "/" + df["Position"] + "/" + df["Team"] # Need to check for duplicate key & find solution
    df['Date'] = datetime.datetime.now()
    # .strftime("%Y-%m-%d %H:%M:%S")

    duplicate_keys=df[df.duplicated(subset=['Key'])][['Name']]
    # if found, update the Name
    # method possible: save exact page number and div allocation for each player
    return df