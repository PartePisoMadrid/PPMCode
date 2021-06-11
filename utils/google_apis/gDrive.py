from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def login(scopes, credentialsPath):
    """
    Signs in google asking for the needed permissions and store the credentials in a file.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentialsPath, scopes)
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

