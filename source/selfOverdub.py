# -*- coding: utf-8 -*-
"""
Created on Fri May 22 09:39:44 2020

@author: utente
"""

def removeSelfOverdub(df):
    import pandas as pd
    
    df = df.sort_values(['id_prog'], ascending = [True])
    projects = df['id_prog'].tolist()
    
    id_ = 0
    remove = []
    for idProg in projects:
        if idProg != id_:
            print(idProg)
            rows = df.loc[df['id_prog'] == idProg]    
            authors = rows['autore_panel'].tolist()
            name = ''
            count = 1
            for auth in authors:
                if auth == name:
                    count = count + 1
                name = auth    
        if count == len(authors):
            
            remove.append(idProg)
        id_ = idProg
    
    removeList = list(dict.fromkeys(remove))
    print('selfOverdub removed = ' + str(len(removeList)))
    print(removeList)
    
    
    for ids in removeList:
       
       rows = df.loc[df['id_prog'] == ids]
       rows = rows.drop_duplicates(subset ="autore_panel",keep='first',inplace=False) 
       rows['project_depth'] = 1
       rows['remixed'] = False
       df = df[df.id_prog != ids]
       df = df.append(rows, ignore_index = True)
       

    return df