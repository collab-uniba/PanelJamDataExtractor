# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 17:57:04 2020

@author: utente
"""
import requests as rq
from bs4 import BeautifulSoup
import re

def searchPanelsId(idProjects,projects_depth):
    
    i = 0 
    panelsId = []
    projectsId = []
    final_projects_depth = []
    remixed = []
    
    while i < len(idProjects):
    #while i < 370:
        count = 0
        while count < projects_depth[i]:
            #final_projects_depth.append(projects_depth[i])
            if count == (projects_depth[i] - 1):
                remixed.append(False)
            else:
                remixed.append(True)
            final_projects_depth.append(count+1)
            projectsId.append(idProjects[i])
            id = str(idProjects[i]) + '_' + str(count+1)
            panelsId.append(id)
            count = count + 1
        i = i + 1
   
    return panelsId,projectsId,final_projects_depth,remixed

        
def panelsAuthors(idProjects):
    #import pandas as pd
    
    projects_depth = []
    firstPanelauthors = []
    authorsNames = []
    removes = []
    count = 0 #X

    print('idProject before:' + str(len(idProjects)))
    
    while count < len(idProjects):
        
        if idProjects[count] != 4759:           
            print(str(count)+"-"+str(idProjects[count]))
            url ="https://www.paneljam.com/jams/"+str(idProjects[count])+"/panels/"
            page1 = rq.get(url)
            authors = []
            #authors2 = []
            soup = BeautifulSoup(page1.content, 'html.parser')
            
                
            strip = soup.find('div', class_ = 'comic-strip group')
            panelsWrap = strip.find_all('div', class_ = 'panel-wrap')
        
            count2 = 0
                
            while count2 < len(panelsWrap):
                img = panelsWrap[count2].find('img')
                if img is not None:
                    author = img['alt']
                    """
                    byOcc = author.count('by')
                    if byOcc > 1:
                        author = author.replace("by","",byOcc - 1)
                    pos = author.find('by')
                    name = author[pos+3:]
                    """
                    pos = author.find('Online Drawing Game Comic Strip Panel by')
                    rep = author[pos:]
                    name = rep.replace('Online Drawing Game Comic Strip Panel by ','')
                    name = name.replace(" ", "%20")
                    name = name.replace("#", "%23")
                    name = name.replace("?", "%3F")                    
                    authors.append(name)
                count2 = count2 + 1
    
            
            
            #Estrazione numero di panels
    
            panels = 0
            for panel in panelsWrap:
                error = panel.find('div', class_ = 'nsfw-panel')
                if error is None:
                    panels = panels + 1
            
            #Estrazione autore primo panel
            if panels > 0:
                primo = authors[0]
                authorsNames.append(primo)
                projects_depth.append(panels)
                firstPanelauthors.append(primo)
                i = 1
                #Estrazione autori panel rimanenti
                while i < panels:
                    firstPanelauthors.append(primo)
                    authorsNames.append(authors[i])
                    i = i + 1  
            else:
                removes.append(count)
                
            count = count + 1
        else:
            removes.append(count)
            count = count + 1
          
    if len(removes) > 0:
        i = 0
        for elem in removes:
            del idProjects[elem - i]
            i = i + 1
            
    return firstPanelauthors,authorsNames,projects_depth,idProjects, removes
 

#FUNZIONE CHE CREA LA PRIMA TABELLA CONTENENTE I PROGETTI E GLI AUTORI DEI PRIMI PANEL E DI TUTTI GLI ALTRI PANEL    
def createFirstTable():
    import modin.pandas as pd
    import time
    from datetime import date,datetime
    
    df = pd.read_excel('C:\\Users\\utente\\Desktop\\PanelJam\\PanelJamDataExtractor\\TabellaProgettiPanelJam.xlsx')
    
    idProjects = (df['project']).tolist()
    #likes = df['Likes']
    #views = df['Views']
    #comments = df['Comments']
    timeProg= (df['Time']).tolist()
    #remixed = df['Remixed']
    
    today = date.today()
    start_time = time.time()
    printTime = time.strftime("%H:%M:%S", time.gmtime(start_time))
    print('Start date: '+ str(today) + ' ' + printTime)
    
    (firstPanelauthors,finalAuthorsNames,projects_depth,idProjects,removes) = panelsAuthors(idProjects)
    
    i = 0
    for elem in removes:
        del timeProg[elem - i]
        i = i + 1

    (panelsId,finalProjectsId,final_projects_depth,mergedRemixed) = searchPanelsId(idProjects, projects_depth)
    
    createMergedTable(firstPanelauthors, finalAuthorsNames, final_projects_depth, panelsId, finalProjectsId, mergedRemixed, idProjects, timeProg)
    
    today = date.today()
    printTime = time.strftime("%H:%M:%S", time.gmtime(time.time()))
    print('End date: '+ str(today) + ' ' + printTime)    
    elapsed_time = time.time() - start_time
    print('Elapsed time: ' + time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    
def mergeRemixed(final_projects_depth):
    
    remixed = []
    for depth in final_projects_depth:
        if depth > 1:
            remixed.append(True)
        else:
            remixed.append(False)
    return remixed

def mergeTime(idProjects,mergedTable,time):
    import modin.pandas as pd
    
    print('mergeTime')
    data = {'id_prog': idProjects,
            'time': time}
    
    df = pd.DataFrame(data, columns = ['id_prog','time'])
    mergedTable = pd.merge(df,mergedTable, on = 'id_prog')

    return mergedTable
    
def mergeAuthors(finalAuthorsNames,firstPanelauthors):

    import Extractor as ex
    #--------------------CREAZIONE TABELLA UTENTI PANEL ATTUALI------------------------------------------------
    noDuplicates = list(dict.fromkeys(finalAuthorsNames))

    shared = ex.shared_projects(noDuplicates)
    (authors_loves, authors_views) = ex.lovesAndViews(noDuplicates,shared)
    stars_list = ex.star_count(noDuplicates)
    avatars = ex.has_avatar(noDuplicates)
    bios = ex.has_bio(noDuplicates)
    nFollowers = ex.followers(noDuplicates)
    
    shared = list(map(int,shared))
    authors_loves = list(map(int,authors_loves))
    authors_views = list(map(int,authors_views))
    stars_list = list(map(int,stars_list))
    nFollowers = list(map(int,nFollowers))
    
    authors_ranking = calculateAuthorRanking(stars_list,authors_loves,authors_views,nFollowers,shared)
    
    authorsTable = createAuthorsTable(noDuplicates,stars_list,avatars,bios,nFollowers,authors_loves,authors_views,authors_ranking,finalAuthorsNames)
    authorsTable = authorsTable.rename(columns = {'Authors':'autore_panel_attuale',
                                                  'Stars':'stars_attuale',
                                                  'Has Avatar':'has_avatar_attuale',
                                                  'Has Bio':'has_bio_attuale',
                                                  'Followers':'followers_attuale',
                                                  'Tot loves':'tot_loves_attuale',
                                                  'Tot views':'tot_views_attuale'})

    #-----------------CREAZIONE TABELLA UTENTI DEI PRIMI PANEL--------------------------------------------------------------
    
    noDuplicates = list(dict.fromkeys(firstPanelauthors))
    firstPanelAuthorsTable = createFirstPanelAuthors(authorsTable, noDuplicates)
    firstPanelAuthorsTable = firstPanelAuthorsTable.rename(columns = {'autore_panel_attuale':'autore_panel_1°',
                                                                      'stars_attuale':'stars_1°',
                                                                      'has_avatar_attuale':'has_avatar_1°',
                                                                      'has_bio_attuale':'has_bio_1°',
                                                                      'followers_attuale':'followers_1°',
                                                                      'tot_loves_attuale':'tot_loves_1°',
                                                                      'tot_views_attuale':'tot_views_1°',
                                                                      'ranking_attuale':'ranking_1°'})
    
   
    #authorsTable.to_excel('authorsTable.xlsx', index = False)
    #firstPanelAuthorsTable.to_excel('firstPanelAuthorsTable.xlsx', index = False)
    return authorsTable, firstPanelAuthorsTable

def calculateAuthorRanking(stars_list,authors_loves,authors_views,nFollowers,shared):
    import modin.pandas as pd
    import numpy as np
    
    stars_list = pd.Series(stars_list)
    authors_loves = pd.Series(authors_loves)
    authors_views = pd.Series(authors_views)
    nFollowers = pd.Series(nFollowers)
    shared = pd.Series(shared)
    
    author_ranking = (stars_list + nFollowers + authors_loves + authors_views)/shared
    author_ranking = author_ranking.fillna(0)
    author_ranking = author_ranking.replace([np.inf, -np.inf],0)
    author_ranking = author_ranking.tolist()
    
    
    return author_ranking

def createFirstPanelAuthors(authorsTable,noDuplicates):
    import modin.pandas as pd
    

    dataAuthors = {'Authors':noDuplicates}
    
    dfAuthors = pd.DataFrame(dataAuthors, columns = ['Authors'])
    mergedAuthors = pd.merge(dfAuthors,authorsTable, left_on = 'Authors', right_on = 'autore_panel_attuale')
    mergedAuthors = mergedAuthors.drop(columns = 'Authors')
    
    return mergedAuthors
    
def createAuthorsTable(noDuplicates,stars_list,avatars,bios,nFollowers,authors_loves,authors_views,authors_ranking,finalAuthorsName):
    import modin.pandas as pd
    
    data = {'Authors': noDuplicates,
            'Stars': stars_list,
            'Has Avatar': avatars,
            'Has Bio': bios,
            'Followers': nFollowers,
            'Tot loves': authors_loves,
            'Tot views': authors_views,
            'ranking_attuale':authors_ranking}
    dataAuthors = {'Authors':finalAuthorsName}
    
    dfAuthors = pd.DataFrame(dataAuthors, columns = ['Authors'])
    df = pd.DataFrame(data, columns = ['Authors','Stars','Has Avatar','Has Bio','Followers','Tot loves','Tot views','ranking_attuale'])
    mergedAuthors = pd.merge(dfAuthors,df, on = 'Authors')
    
    return mergedAuthors  
    
def createMergedTable(firstPanelauthors, finalAuthorsNames, final_projects_depth, panelsId, finalProjectsId,mergedRemix, idProjects, time):
    import modin.pandas as pd
    import gc
    print('createMergedTable')
    data = {'id_prog': finalProjectsId,
            'id_panel': panelsId,
            'project_depth': final_projects_depth,
            'remixed': mergedRemix,
            'autore_panel_1°': firstPanelauthors,
            'autore_panel_attuale':finalAuthorsNames}
    mergedTable = pd.DataFrame(data, columns = ['id_prog','id_panel','project_depth','remixed','autore_panel_1°','autore_panel_attuale'])    
    mergedTable = mergeTime(idProjects,mergedTable,time)
    #mergedTable.to_excel('mergedTable.xlsx', index = False)
    authorsTable,firstPanelAuthorsTable = mergeAuthors(finalAuthorsNames,firstPanelauthors)
    memory = gc.collect()
    print(memory)
    tableWithAuthorsPanels = createTableWithAuthorsPanels(authorsTable, mergedTable)
    createFinalTable(tableWithAuthorsPanels,firstPanelAuthorsTable)
    
    
def createTableWithAuthorsPanels(authorsTable,mergedTable):
    import modin.pandas as pd
    
    tableWithAuthorsPanels = pd.merge(mergedTable,authorsTable, on = 'autore_panel_attuale')
    tableWithAuthorsPanels = tableWithAuthorsPanels.drop_duplicates(subset = "id_panel")
    return tableWithAuthorsPanels    

def createFinalTable(tableWithAuthorsPanels,firstPanelAuthorsTable):   
    import modin.pandas as pd
    
    finalTable = pd.merge(tableWithAuthorsPanels,firstPanelAuthorsTable, on = 'autore_panel_1°')
    
    finalTable = finalTable.drop_duplicates(subset = "id_panel")
    finalTable.to_excel('C:\\Users\\utente\\Desktop\\PanelJam\\PanelJamDataExtractor\\PanelJamTable.xlsx', index = False)


def mergePanelsFeature():
    import modin.pandas as pd
    
    projectTable = pd.read_excel("C:\\Users\\utente\\Desktop\\PanelJam\\PanelJamDataExtractor\\TabellaProgettiPanelJam.xlsx")    
    PanelJamTable = pd.read_excel("C:\\Users\\utente\\Desktop\\PanelJam\\PanelJamDataExtractor\\PanelJamTable.xlsx")    
        
    Table = pd.merge(PanelJamTable,projectTable, left_on = 'id_prog', right_on = 'project')
    Table = Table.drop(columns = ['project','Remixed','Time','Project depth'])
    
    Table.to_excel("C:\\Users\\utente\\Desktop\\PanelJam\\PanelJamDataExtractor\\TabellaCompleta.xlsx",index = False)