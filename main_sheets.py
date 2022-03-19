from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

# The ID and range of the spreadsheet
SPREADSHEET_ID = '1u40di-ObKV-K0zBD3DHOAZJrBAWLnKe-8Cck6xD48_8'
RANGE_NAME = 'Sheet1!A1:B'

# Get credentials from the token file
creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])
print(values)