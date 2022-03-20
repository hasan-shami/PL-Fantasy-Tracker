import pandas as pd
import gspread
from df2gspread import df2gspread as d2g
from df2gspread import gspread2df as g2d
import gspread_dataframe as gd
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'jsonFileFromGoogle.json', scope)
gc = gspread.authorize(credentials)

spreadsheet_key = '1u40di-ObKV-K0zBD3DHOAZJrBAWLnKe-8Cck6xD48_8'
wks_name = 'Master'


def download_sheet(sheet):
    # Download df
    dfd = g2d.download(spreadsheet_key, sheet, credentials=credentials, col_names=True)
    return dfd


def upload_sheet(df, sheet):
    # Upload existing data
    d2g.upload(df, spreadsheet_key, sheet, credentials=credentials, row_names=False, col_names=True)


def append_rows(df, sheet):
    sh = gc.open_by_key(spreadsheet_key)
    json_df = df.copy()  # JSON specific formatting for upload
    json_df['Date'] = json_df['Date'].astype(str)
    json_df = json_df.fillna('')
    values = json_df.values.tolist()
    sh.values_append(sheet, {'valueInputOption': 'USER_ENTERED'}, {'values': values})


def clear_sheet(sheet):
    sh = gc.open_by_key(spreadsheet_key)
    sh.values_clear(sheet)
