
def writeCell(service, cellvalue, spreadsheet_id, worksheet_name, cell_range_insert, value_input_option):
    """
    Update a given cell of a worksheet with a given value
    """
    values = [
    [
        # cell values ...
        cellvalue,
    ],
        # additional rows ...
    ]
    body = {
        'values': values
    }
    range_name = worksheet_name + "!" + cell_range_insert
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))