import pandas as pd


def check_price_change(df):
    df['Cost_old'] = df['Cost_old'].astype(int, errors='raise')
    cost_df = df.loc[~(df['Cost_new'] == df['Cost_old'])][['Key', 'Cost_new', 'Cost_old']]
    return cost_df


def check_form_change(df):
    df['Form_old'] = df['Form_old'].astype(int, errors='raise')
    form_df = df.loc[~(df['Form_new'] == df['Form_old'])][['Key', 'Form_new', 'Form_old']]
    return form_df


def check_points(df):
    df['Points_old'] = df['Points_old'].astype(int, errors='raise')
    points_df = df.loc[~(df['Points_new'] == df['Points_old'])][['Key', 'Points_new', 'Points_old']]
    return points_df


def check_differences(df, master_df, price_only):
    last_run_date = master_df['Date'].max()
    last_run_df = master_df[master_df['Date'] == last_run_date]
    if price_only:  # Hourly
        merged_df = df.merge(last_run_df[['Cost', 'Key', 'Date']], how='left',
                             on='Key',
                             suffixes=('_new', '_old'))
        cost_df = check_price_change(merged_df)
        print(cost_df)
        # maybe: if cost df not empty, update the entire dfs
    else:  # Once Daily or Twice Daily
        merged_df = df.merge(last_run_df[['Cost', 'Selected By %', 'Form', 'Points', 'Key', 'Date']], how='left',
                             on='Key',
                             suffixes=('_new', '_old'))
        form_df = check_form_change(merged_df)
        points_df = check_points(merged_df)
        cost_df = check_price_change(merged_df)
