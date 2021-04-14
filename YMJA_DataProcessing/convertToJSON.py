from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import os
from datetime import date

today = date.today()
formatted_date = today.strftime("%Y-%m-%d")

# NOTE Remember to run the transcript file before to update the CC
# TODO Run the transcript program from here

DEFAULT_PATH = "/usr/local/data02/dpdataset/DP17_PostProcessing/json/{}-penalties.json".format(formatted_date)

# NOTE Could read them from the excel sheet, but for simplicity encode them manually
PENALTYTYPES = {
   "No penalty": 0,
   "Tripping": 1,
   "Hooking": 2,
   "Slashing": 3,
   "Roughing": 4,
   "Interference": 5,
   "Holding": 6,
   "Cross-checking": 7,
   "Hi sticking": 8,
}

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1hiSfVo1CNPE-e4vOZGSK15hBC1pDaPo67QCA7QQJTOM'
READ_RANGE_NAME = ['Michel!A:G', 'Cyril!A:G', 'Alex!A:G', 'Ben!A:G']

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # TODO Call transcript extraction file
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    acc=[]
    for range_name in READ_RANGE_NAME: 
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=range_name).execute()
        values = result.get('values', [])
        acc += values[1:]
        print('{0} rows retrieved.'.format(len(values)))

    create_json_file(acc)

def create_json_file(values, dest=DEFAULT_PATH):
    data = {"penalties": []}
    i=0
    for row in values:
        i+=1
        # NOTE All columns must be filled and formatted correctly.
        videoname, penalty_number, penalty_name = row[0].split(".")[0], PENALTYTYPES[row[3]], row[3]
        start, end = row[1], row[2]

        data["penalties"].append({"ID": i, "gamename": videoname, "start": start, "end": end, "penalty_number": penalty_number, "label": penalty_name, "distance": row[4], "CC": row[5], "replay": row[6]})

    with open(dest,"w") as f:
        json.dump(data,f,indent=4)
    print('{} rows written.'.format(len(values)))

if __name__ == '__main__':
    main()