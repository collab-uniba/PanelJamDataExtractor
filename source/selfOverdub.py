# -*- coding: utf-8 -*-
"""
Created on Fri May 22 09:39:44 2020

@author: utente
"""

def removeSelfOverdub(df):
    import pandas as pd
    
    #df = pd.read_excel('C:\\Users\\utente\\Desktop\\PanelJam\\PanelJamDataExtractor\\data\\TabellaCompleta2Pulita.xlsx', index = False)
    #df = pd.read_excel('..\\data\\TabellaCompleta.xlsx', index = False)

    df = df.sort_values(['id_prog'], ascending = [True])
    projects = df['id_prog'].tolist()
    #df = df.set_index('id_prog')
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
            #df = df.drop(idProg,axis = 0)
            remove.append(idProg)
        id_ = idProg
    
    removeList = list(dict.fromkeys(remove))
    print('selfOverdub removed = ' + str(len(removeList)))
    print(removeList)
    
    #df2 = df.set_index('id_prog')
    for ids in removeList:
       #df2 = df2.drop(ids, axis=0)
       rows = df.loc[df['id_prog'] == ids]
       rows = rows.drop_duplicates(subset ="autore_panel",keep='first',inplace=False) 
       rows['project_depth'] = 1
       rows['remixed'] = False
       df = df[df.id_prog != ids]
       df = df.append(rows, ignore_index = True)
       
       
    #df2 = df2.reset_index()
    #df2.to_excel('C:\\Users\\utente\\Desktop\\PanelJam\\PanelJamDataExtractor\\data\\TabellaSenzaSelfOverdub.xlsx', index = False)
    #df.to_excel('..\\data\\TabellaCompleta.xlsx', index = False)
    return df