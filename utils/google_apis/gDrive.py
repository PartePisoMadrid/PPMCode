from __future__ import print_function
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def login(scopes, credentialsPath):
    """
    Signs in google asking for the needed permissions and store the credentials in a file.
    """
    creds = None
    # the file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    # if there are no (valid) credentials available, let the user log in.
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

def printFirstFiles(service, n):
    """
    Prints the names and ids of the first n files the user has access to.
    """
    # call the Drive v3 API
    results = service.files().list(
        pageSize=n, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

def title2id(service, fileName):
    """
    Gets the id that correspond to a file name.
    """
    results = service.files().list(q="name='"+fileName+"'",
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if len(items)==0:
        raise Exception("There are not files with the title "+fileName+" in the gDrive account")
    if len(items)!=1:
        raise Exception("There must not be more than one ID associated to the name specified")
    return items[0]['id']

def giveAccess(service, fileId, type, emailAddress=None, emailMessage=None):
    """
    give privileges to edit fileId
    """
    user_permission = ({
                        'type': type,
                        'role': 'writer',
                        'emailAddress': emailAddress,
                        })
    service.permissions().create(fileId=fileId,body=user_permission,fields='id', emailMessage=emailMessage).execute()