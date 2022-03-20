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


def download_sheet():
    # Download df
    dfd = g2d.download(spreadsheet_key, wks_name, credentials=credentials, col_names=True)
    return dfd


def upload_sheet(df):
    # Upload existing data
    d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=False, col_names=True)

def append_rows(df):
    sh = gc.open_by_key(spreadsheet_key)
    df['Date'] = df['Date'].astype(str)
    df=df.fillna('')
    values = df.values.tolist()
    sh.values_append(wks_name,{'valueInputOption': 'USER_ENTERED'},{'values': values})
