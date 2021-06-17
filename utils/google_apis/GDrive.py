
def printFirstFiles(service, n):
    """
    Prints the names and ids of the first n files the user has access to.
    """
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