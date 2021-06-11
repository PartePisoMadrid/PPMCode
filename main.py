#!/home/ebotiab/anaconda3/bin/python

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 09:59:29 2020

@author: PartePisoMadrid
"""
import numpy as np
import pandas as pd
import datetime
import subprocess, sys
import os

from openpyxl import load_workbook
import smtplib

from utils.FileConvert import gsheet2csv
from utils.FileConvert import csv2excel

## CONSTANTS
CREDENTIALS_PATH = "/home/ebotiab/Desktop/parte/credentials/"

def printParte():
    # update Parte url if it is monday
    reviseWeekDay = datetime.datetime.today().weekday()
    if reviseWeekDay==0:
        ff = open("Parte_files/url_parte.txt", "w")
        writeWithTKinter(ff, 'Copy here the new Parte url')

    fileToRead = open("Parte_files/url_parte.txt", "r")
    parteUrl = fileToRead.read()
    fileToRead.close()

    # download Parte google sheet to a csv
    parteCsv = gsheet2csv(CREDENTIALS_PATH, parteUrl, 5, 'Parte_files/resumen.csv') 
    # convert csv downloaded to excel
    parteDf = csv2excel("Parte_files/resumen.csv", 'Parte_files/resumen_data.xlsx', 'Sheet1') 
    # store date
    weekDay = parteDf.columns[2]

    # load workbook 
    wb_to_write = load_workbook('Parte_files/RESUMEN_PARTE.XLSX')
    # get sheets of the woorkbooks
    sheet_to_read = load_workbook('Parte_files/resumen_data.xlsx')['Sheet1']
    sheet_to_write = wb_to_write['Resumen_cocina']

    # update content of RESUMEN_PARTE.xlsx
    for row_read in range(2,23):
        row_write = row_read
        
        if row_write>12:
            row_write+=2
        if row_write>21:
            row_write+=1
        
        for col in range(3,8):
            if type(sheet_to_write.cell(row_write,col)).__name__ == 'MergedCell':
                continue
            sheet_to_write.cell(row_write,col).value = ""
            if type(sheet_to_read.cell(row_read,col).value)!=tuple:
                value = sheet_to_read.cell(row_read,col).value
                to_center = ["TU","TB","AF2","AF3"]
                if value in to_center:
                    value = "                       " + value
                if value=="AF2 + AF3":
                    value = "                   " + value
                sheet_to_write.cell(row_write,col).value = value
            print('row: '+str(row_read)+' col: '+str(col)+' value: '+str(sheet_to_read.cell(row_read,col).value))
    
    #save the changes in other xlsx file
    sheet_to_write.cell(1,3).value = weekDay
    wb_to_write.save("Parte_files/RESUMEN_IMPRIMIBLE.xlsx")
    
    # convert excel to pdf
    os.system("soffice --headless --convert-to pdf Parte_files/RESUMEN_IMPRIMIBLE.xlsx")
    #move to Parte_files folder
    os.rename("RESUMEN_IMPRIMIBLE.pdf", "Parte_files/RESUMEN_IMPRIMIBLE.pdf") 
    # print pdf
    os.system("lp Parte_files/RESUMEN_IMPRIMIBLE.pdf")

def main():
    # download and print Parte
    printParte()
    

if __name__ == '__main__':
	main()