from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os.path

def login(scopes, credentialsPath):
    """
    Signs in google asking for the needed permissions and store the credentials in a file.
    """
    creds = None
    tokenPath = credentialsPath+'token.json'
    clientSecretPath = credentialsPath+"client_secrets.json"
    # the file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(tokenPath):
        creds = Credentials.from_authorized_user_file(tokenPath, scopes)
    # if there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        refresh = False
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        except:
            refresh = True
        if not (creds and creds.expired and creds.refresh_token) or refresh:
            flow = InstalledAppFlow.from_client_secrets_file(
                clientSecretPath, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenPath, 'w') as token:
            token.write(creds.to_json())
    return creds