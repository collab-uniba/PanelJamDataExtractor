# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 10:45:22 2020

@author: utente
"""
def deEmojify(inputString):

    return inputString.encode('ascii', 'ignore').decode('ascii')    

def cleanAuthors(col):
    
    import cleantext as cl
    import openpyxl as xl
    
    wb = xl.load_workbook("..\\data\\TabellaCompleta.xlsx")
    ws = wb.active
    count = 0
    for row in ws.rows:
        if count >= 1:
            row[col].value = deEmojify(row[col].value)
            row[col].value = cl.clean(row[col].value,no_line_breaks = True,
                         no_urls = True,
                         replace_with_url ="<URL>",
                         no_digits = True,
                         no_currency_symbols = True,
                         no_punct = True,
                         no_numbers = True,
                         replace_with_number = "")
            if '0' in row[col].value:
                row[col].value = (row[col].value).replace('0','')
        count = count + 1
    print("cleanAuthors exeuted:")    
    wb.save("..\\data\\TabellaCompleta.xlsx")

def cleanProjects(file):
    import cleantext as cl
    import openpyxl as xl
    
    wb = xl.load_workbook("C:\\Users\\utente\\Desktop\\PanelJam\\PanelJamDataExtractor\\data\\" + file + ".xlsx")
    ws = wb.active
    
    for row in ws.rows:
    
        row[0].value = cl.clean(row[0].value,no_line_breaks = True,
                     no_digits = False,
                     no_punct = True)
        row[0].value = (row[0].value).replace('jams','')
        row[0].value = (row[0].value).replace('panels','')
    
    #trasformazione data di creazione progetti

    for row in ws.rows:
        val = row[6].value
        row[6].value = timeChanger(val)
            
    print("cleanProjects exeuted:\n")    
    value = input('Please insert file name: ')
    wb.save("C:\\Users\\utente\\Desktop\\PanelJam\\PanelJamDataExtractor\\data\\" + value + ".xlsx")            
            
            
def timeChanger(val):
    
    switcher = {
            'about 1 month ago': '45 days ago',
            'about 2 months ago': '75 days ago',
            '2 months ago': '60 days ago',
            '3 months ago': '90 days ago',
            '4 months ago': '120 days ago',
            '5 months ago': '150 days ago',
            '6 months ago': '180 days ago',
            '7 months ago': '210 days ago',
            '8 months ago': '240 days ago',
            '9 months ago': '270 days ago',
            '10 months ago': '300 days ago',
            '11 months ago': '330 days ago',
            '12 months ago': '365 days ago',
            'almost 1 year ago': '350 days ago',
            'almost 2 years ago': '710 days ago',
            'almost 3 years ago': '1060 days ago',
            'almost 4 years ago': '1430 days ago',
            'about 1 year ago': '450 days ago',
            'about 2 years ago': '800 days ago',
            'about 4 years ago': '1550 days ago',
            'over 1 year ago' : '530 days ago',
            'over 2 years ago': '880 days ago'
                }
    if val in switcher:
        return switcher.get(val)
    else:
        return val
    
    
    
    
    
    
    
    
    
    
    