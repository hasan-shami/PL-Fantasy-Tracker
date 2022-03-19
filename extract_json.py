import requests
import pandas as pd
import datetime
import time


def get_data(data):
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    r = requests.get(url)
    json = r.json()
    json.keys()
    if data == 'all':
        players_df = pd.DataFrame(json['elements'])
        types_df = pd.DataFrame(json['element_types'])
        teams_df = pd.DataFrame(json['teams'])
        return players_df, types_df, teams_df
    elif data == 'teams/types':
        types_df = pd.DataFrame(json['element_types'])
        teams_df = pd.DataFrame(json['teams'])
        return types_df, teams_df
    elif data == 'players':
        players_df = pd.DataFrame(json['elements'])
        return players_df


def initialize_codes(automated):
    # This function is for setting up codes for the first time. The idea is to implement this manually once per season
    # to save computation time
    if automated:
        types_df, teams_df = get_data('teams/types')
        shortened_teams_df = teams_df[['code', 'short_name']]
        shortened_types_df = types_df[['id', 'plural_name_short']]
    else:  # Manually (might want to explore the option of downloading from sheets)
        shortened_teams_data = {'team_code': [3, 7, 94, 36, 90, 8, 31, 11, 13, 2, 14, 43, 1, 4, 45, 20, 6, 57, 21, 39],
                                'Team': ['ARS', 'AVL', 'BRE', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LEE',
                                         'LIV', 'MCI', 'MUN', 'NEW', 'NOR', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']}
        shortened_teams_df = pd.DataFrame(shortened_teams_data)

        shortened_types_data = {'element_type': [1, 2, 3, 4], 'Position': ['GKP', 'DEF', 'MID', 'FWD']}
        shortened_types_df = pd.DataFrame(shortened_types_data)
    return shortened_teams_df, shortened_types_df


def get_players_data():
    players_df = get_data('players')
    df = players_df[['first_name', 'web_name', 'element_type', 'team_code', 'chance_of_playing_next_round', 'now_cost',
                     'selected_by_percent', 'form', 'total_points']]
    shortened_teams_df, shortened_types_df = initialize_codes(automated=False)
    df = df.merge(shortened_teams_df, how='left', on='team_code')
    df = df.merge(shortened_types_df, how='left', on='element_type')
    df.drop(columns=['team_code', 'element_type'], inplace=True)

    # Formatting to match existing template
    df = df.rename(columns={'web_name': 'Name', 'element_type': 'Position', 'team_code': 'Team',
                            'chance_of_playing_next_round': 'Playing Chance', 'now_cost': 'Cost',
                            'selected_by_percent': 'Selected By %', 'form': 'Form', 'total_points': 'Points'})
    cols = df.columns.tolist()
    reordered_cols_indices = [0, 1, -1, -2, 2, 3, 4, 5, 6]
    reordered_cols = [cols[i] for i in reordered_cols_indices]
    df = df[reordered_cols]

    df['Cost']=df['Cost']/10

    # Before creating key, checking for duplicates (Note: for next season, just use player ids for Key.)
    if df.duplicated(subset=['Name', 'Team', 'Position']).any():
        indices = df.index[df.duplicated(subset=['Name', 'Team', 'Position'], keep=False)].tolist()
        for i in indices:
            df.iloc[i, 1] = df.iloc[i, 0] + " " + df.iloc[i, 1]
    df.drop(columns=['first_name'], inplace=True)

    df['Key'] = df['Name'] + "/" + df["Position"] + "/" + df["Team"]
    df['Date'] = datetime.datetime.now()
    return df
