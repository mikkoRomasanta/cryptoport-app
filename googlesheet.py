from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime
import os


load_dotenv()

# Setup spreadsheet info
service_account_file = 'keys.json'
scopes = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)
spreadsheet_id = os.getenv('SPREADSHEET_ID')
spreadsheet_range = os.getenv('SPREADSHEET_RANGE')
spreadsheet_range_dt = os.getenv('SPREADSHEET_RANGE_DT')
service = build('sheets', 'v4', credentials=creds)

sheet = service.spreadsheets()

def send_to_sheet(quotes):
    '''Updates the google sheet file with latest token data'''
    #--- UPDATE COINS ---
    sheet.values().update(spreadsheetId=spreadsheet_id,range=spreadsheet_range,
                                        valueInputOption='USER_ENTERED', body={'values':quotes}).execute()

    #--- UPDATE DATE/TIME UPDATED ---
    dt = datetime.datetime.now()
    dt_json = [['timestamp', dt.strftime('%Y-%m-%dT%Hh:%Mm:%Ss.%f')]]

    sheet.values().update(spreadsheetId=spreadsheet_id,range=spreadsheet_range_dt,
                                        valueInputOption='USER_ENTERED', body={'values':dt_json}).execute()
    
    message = f'--- updated {len(quotes)} tokens. {dt} ---'
    
    return message