from main_sheets_gspread import *
from differences import *
from extract_webdriver import *
from extract_json import *


def export_results(df, mode, upload_all):
    if mode == 'excel':
        master_df = pd.read_excel("FPL_Master.xlsx")
        master_df = master_df.append(df)
        master_df.to_excel("FPL_Master.xlsx", index=False)
    if mode == 'sheets':
        if upload_all:
            master_df = download_sheet()
            master_df_new = master_df.copy().append(df)
            master_df_new.reset_index(inplace=True, drop=True)
            upload_sheet(master_df_new, 'Master')
            return master_df
        else:
            append_rows(df, 'Master')
            clear_sheet('Last')
            upload_sheet(df, 'Last')


if __name__ == "__main__":
    # Standard function, run every hour
    implementation = 'json'

    if implementation == 'scrape':
        driver = initialize_driver()
        players_list = get_player_standard(driver)
        df = format_players(players_list)
    elif implementation == 'json':
        df = get_players_data()
    # master_df = export_results(df, 'sheets', upload_all = False)
    old_df = export_results(df, 'sheets', upload_all=False)
    check_differences(df, old_df, price_only=False)
