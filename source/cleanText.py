# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 10:45:22 2020

@author: utente
"""

def cleanAuthorsNames():
    import cleantext as cl
    import openpyxl as xl
    
    wb = xl.load_workbook("C:\\Users\\utente\\Desktop\\PanelJam\\PanelJamDataExtractor\\TabellaAutoriPanelJam.xlsx")
    ws = wb.active
    #names = []
    for row in ws.rows:
    
        row[0].value = cl.clean(row[0].value,no_line_breaks = True,
                     no_urls = True,
                     replace_with_url ="<URL>",
                     no_digits = True,
                     no_currency_symbols = True,
                     no_punct = True,
                     no_numbers = True,
                     replace_with_number = "")
        if '0' in row[0].value:
            row[0].value = (row[0].value).replace('0','')
        
    wb.save("C:\\Users\\utente\\Desktop\\PanelJam\\PanelJamDataExtractor\\TabellaAutoriPanelJam.xlsx")
    
def cleanProjectsNames():
    import cleantext as cl
    import openpyxl as xl
    
    wb = xl.load_workbook("C:\\Users\\utente\\Desktop\\PanelJam\\PanelJamDataExtractor\\TabellaProgettiPanelJam.xlsx")
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
            
    
    wb.save("C:\\Users\\utente\\Desktop\\PanelJam\\PanelJamDataExtractor\\TabellaProgettiPanelJam.xlsx")            
            
            
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
            'almost 1 year ago': '350 days ago',
            'almost 2 years ago': '710 days ago',
            'almost 3 years ago': '1060 days ago',
            'almost 4 years ago': '1430 days ago',
            'about 1 year ago': '530 days ago',
            'about 2 years ago': '880 days ago',
            'about 4 years ago': '530 days ago',
            'over 1 year ago' : '450 days ago',
            'over 2 years ago': '800 days ago'
                }
    if val in switcher:
        return switcher.get(val)
    else:
        return val
    
    
    
    
    
    
    
    
    
    
    