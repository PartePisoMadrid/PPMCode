import numpy as np
import pandas as pd
import os
from gsheets import Sheets
from pathlib import Path

def gsheet2csv(filespath, gsheetURL, sheetNumber, csvFileName):
    """
    Export google sheet to csv file
    """
    gsheets = Sheets.from_files(filespath+'client_secrets.json', filespath+'storage.json')
    sheet = gsheets.get(gsheetURL) #get sheet in a SpreadSheet object
    sheet.sheets[sheetNumber].to_csv(csvFileName, encoding='utf-8', dialect='excel') #to csv
    return sheet

def csv2excel(csvFileName, excelFileName, sheetName):
    """
    Read a csv file as and save it as excel file, returns a dataframe with the csv data
    """
    df = pd.read_csv(csvFileName) # load csv
    writer = pd.ExcelWriter(excelFileName,engine='xlsxwriter') # specify a writer
    df.to_excel(writer, sheetName) # write your DataFrame to a file
    writer.save() # save the result
    return df
