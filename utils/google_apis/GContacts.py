def getGroupData(service, groupName, attList):
    """
    get needed data about the group of contacts specified with groupName
    """
    # import IPython ; IPython.embed() ; exit(); 
    groupsDataList = service.contactGroups().list().execute()["contactGroups"]
    for group in groupsDataList:
        if group["name"] == groupName:
            groupData = []
            for att in attList:
                groupData.append(group[att])
    return groupData


def getContactsData(service, groupResourceName, maxMembers):
    """
    get names and mails of the contacts inside the specified group
    """
    # get the ids of the contacts inside the specified group
    contactsIDs = service.contactGroups().get(
        resourceName=groupResourceName, 
        maxMembers=maxMembers).execute()["memberResourceNames"]

    # get data of the contacts that correspond to the ids obtained
    contactsData = service.people().getBatchGet(
            resourceNames=contactsIDs,
            personFields='names,emailAddresses').execute()["responses"]

    # extract the names and the emailAddresses of the contacts
    namessList = [] 
    mailsList = []
    for contact in contactsData:
        try:
            namessList.append(contact["person"]["names"][0]["displayName"])
        except:
            raise Exception("All contacts must have a name associated")
        mailsList.append(contact["person"]["emailAddresses"][0]["value"])
    return namessList, mailsList
