from differences import *
from main import *

if __name__ == "__main__":
    # Standard function, run every hour
    implementation = 'json'
    if implementation == 'scrape':
        driver = initialize_driver()
        players_list = get_player_standard(driver)
        df = format_players(players_list)
    elif implementation == 'json':
        df = get_players_data()
    master_df = download_sheet()
    check_differences(df, master_df, price_only=True)