from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from datetime import datetime, timedelta

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
# chante path as appropriate
CREDENTIALS_PATH = '/home/ebotiab/Desktop/parte/credentials'

FILE_ID = "1KKsoosB88DlOIHgBkd4K9iQxbPeUvWmvB_u9RhuJ2N8"
FOLDER_ID = "1xYJf9E9oRs3cvtdSNFLo3qolo8438lR4"

SPANISH_MONTH = {1:"enero", 2:"febrero", 3:"marzo", 4:"abril", 5:"mayo", 6:"junio", 7:"julio", 8:"agosto", 9:"septiembre", 10:"octubre",11:"noviembre", 12:"diciembre"}

def login():
    """
    Signs in google asking for the needed permissions and store the credentials in a file.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def printFirstFiles(creds, n):
    """
    Prints the names and ids of the first n files the user has access to.
    """
    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=n, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

def title2ids(service, fileName):
    """
    Gets the ids that correspond to a file name.
    """
    results = service.files().list(q="name='"+fileName+"'",
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    ids = []
    if not items:
        print('No files found.')
    else:
        for item in items:
            ids += [item['id']]
        return ids


def writeCellGSheet(service, cellvalue, spreadsheet_id, worksheet_name, cell_range_insert, value_input_option):
    """
    update a given cell of a worksheet with a given value
    """
    values = [
    [
        # Cell values ...
        cellvalue,
    ],
        # Additional rows ...
    ]
    body = {
        'values': values
    }
    range_name = worksheet_name + "!" + cell_range_insert
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

def main():
    """
    creates Parte for next week
    """
    print("Creating new Parte...")
    creds = login()
    # call the Drive v3 API
    service = build('drive', 'v3', credentials=creds)
    # copy the template file
    service.files().copy(fileId=FILE_ID,
                body={"parents": [{"kind": "drive#fileLink", "id": FOLDER_ID}]}).execute()
    # get id from copy
    ids = title2ids(service, "Copia de Parte_Coronavirus")
    if len(ids)!=1:
        raise Exception("There must be a unique ID associated to the name specified")
    # rename copy with date of next monday
    now = datetime.now()
    monday = now + timedelta(days = 7-now.weekday())
    copyTitle = "Semana "+str(monday.day)+" de "+ SPANISH_MONTH[monday.month]
    service.files().update(fileId=ids[0], body={"name":copyTitle}).execute()
    # call the GSheets v4 API
    service = build('sheets', 'v4', credentials=creds)
    # modify copy by changing the dates
    dateToInsert = str(monday.day)+"/"+str(now.month)+"/"+str(now.year)
    writeCellGSheet(service, dateToInsert, ids[0], "Parte", "E3:G3", "USER_ENTERED")
    print("Parte called "+copyTitle+" has been successfully created")

if __name__ == '__main__':
    main()