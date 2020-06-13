# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 16:45:42 2020

@author: utente
"""

import requests as rq
import time
from bs4 import BeautifulSoup

def featuresExtractor():
    from datetime import date,datetime
    import cleanText as clean
    today = date.today()
    start_time = time.time()
    printTime = time.strftime("%H:%M:%S", time.gmtime(start_time))
    print('Start date: '+ str(today) + ' ' + printTime)
    
    
    totProjects = findProjects()
    #Estrazione features dei progetti    
    (remixed_list, project_depth_list, time_list, comments_list, likes_list, views_list) = project_stats(totProjects)
    createProjectsTable(totProjects,remixed_list,likes_list,views_list,comments_list,project_depth_list,time_list)
    clean.cleanProjects()
    
    today = date.today()
    printTime = time.strftime("%H:%M:%S", time.gmtime(time.time()))
    print('End date: '+ str(today) + ' ' + printTime)    
    elapsed_time = time.time() - start_time
    print('Elapsed time: ' + time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

def createProjectsTable(totProjects,remixed_list,likes_list,views_list,comments_list,project_depth_list,time_list):
    import pandas as pd
    
    data = {'Project': totProjects,
            'Remixed': remixed_list,
            'Likes': likes_list,
            'Views': views_list,
            'Comments': comments_list,
            'Project depth': project_depth_list,
            'Time': time_list}
    df = pd.DataFrame(data, columns = ['Project','Remixed','Likes','Views','Comments','Project depth','Time'])
    df.to_excel('..\\data\\TabellaProgettiPanelJam.xlsx', index = False)    
    
def createAuthorsTable(authors_list,stars_list,avatars,bios,nFollowers,authors_loves,authors_views,shared):
    import pandas as pd
    
    data = {'Authors': authors_list,
            'Stars': stars_list,
            'Has Avatar': avatars,
            'Has Bio': bios,
            'Followers': nFollowers,
            'Tot loves': authors_loves,
            'Tot views': authors_views,
            'Shared projects':shared}
    df = pd.DataFrame(data, columns = ['Authors','Stars','Has Avatar','Has Bio','Followers','Tot loves','Tot views','Shared projects'])
    df.to_excel('TabellaAutoriPanelJam.xlsx', index = False)
        
def star_count(authors_list):
    stars_list = []
    print('star_count function started')
    i = 0
    while i < len(authors_list):
        try:
            url ="https://www.paneljam.com/"+authors_list[i]
            page1 = rq.get(url)
            soup = BeautifulSoup(page1.content, 'html.parser')
            
            #Ricerca per tag e class per estrapolare la feature star_count
            stars = soup.find('div', class_='star-count').get_text()
            stars_list.append(stars)
            print(stars)
            i = i + 1
        except rq.ConnectionError:
            time.sleep(60)

    return stars_list

#Funzione che restitusice true se l'utente ha un avatar diverso da quello di default, altrimenti false
def has_avatar(authors_list):
    
    avatars=[]
    print('has_avatar function started')
    i = 0
    while i < len(authors_list):
        try:
            url = "https://www.paneljam.com/"+authors_list[i]
            page = rq.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            profile = soup.find('div', class_ = 'avatar-wrap')
            avatar = profile.find(class_='avatar-render')
            ref = avatar['src']
            if 'no-avatar-mid' in ref:
                avatars.append('False')
                print('False')
            else:
                avatars.append('True')
                print('True')
            i = i + 1
        except rq.ConnectionError:
            time.sleep(60)
        
            
    return avatars

#Funzione che restitusice true se l'utente ha una bio, altrimenti false
def has_bio(authors_list):
    bios=[]
    print('has_bio function started')
    i = 0
    while i < len(authors_list):
        try:
            url = "https://www.paneljam.com/"+authors_list[i]
            page = rq.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            profile = soup.find('p', class_ = 'txt-center')
            
            if profile is None:
                bios.append('False')
                print('False')
            else:
                bios.append('True')
                print('True')
            i = i + 1
        except rq.ConnectionError:
            time.sleep(60)

    return bios     

def followers(authors_list):
    nFollowers=[]
    print('followers function started')
    i = 0
    while i < len(authors_list):
        try:
            url = "https://www.paneljam.com/"+authors_list[i]
            page = rq.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            profile_menu = soup.find('div', class_ = 'profile__menu')
            if profile_menu is not None:
                friends_list = profile_menu.find('a',href=re.compile('/friends'))
                print(authors_list[i]+' friends: ' + friends_list.get_text())
                friends = friends_list.get_text()
                nFollowers.append(friends)
            else:
                print(authors_list[i]+' friends: ' + '0')
                nFollowers.append('0')
            i = i + 1
        except rq.ConnectionError:
            time.sleep(60)

    return nFollowers

def project_stats(totProjects):
    import re
    
    remixed_list = []
    likes_list = []
    views_list = []
    comments_list = []
    project_depth_list = []
    time_list = []
    i = 0
    
    while i < len(totProjects):
        try:
            url = "https://www.paneljam.com"+totProjects[i]
            page = rq.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            project = soup.find("div", class_ = "action-bar")
            stats = project.find("div", class_ = "right")

            panelsTag = stats.find('img', alt = 'Comic Panel Count Icon')
            timeTag = stats.find('img', alt = 'Time Since Completed Icon')
            commentsTag = stats.find('img', alt = 'Comic Comments Count Icon')
            likesTag = stats.find('img', alt = 'Likes Count Icon')
            viewsTag = stats.find('img', alt = 'Views Count Icon')
            spans = stats.find_all('span')

            for span in spans:

                #Ricerca numero vignette per un progetto
                if str(panelsTag) in str(span):
                    panels = int(re.search(r'\d+', span.get_text()).group())
                    project_depth_list.append(panels)
                    if panels > 1:
                        remixed_list.append('True')
                    else:
                        remixed_list.append('False')

                #Ricerca tempo di creazione del progetto
                if str(timeTag) in str(span):
                    time_list.append(span.get_text())

                #Ricerca numero di commenti di un progetto
                if str(commentsTag) in str(span):
                    comments = int(re.search(r'\d+', span.get_text()).group())
                    comments_list.append(comments)

                #Ricerca numero di likes di un progetto
                if str(likesTag) in str(span):
                    likes = int(re.search(r'\d+', span.get_text()).group())
                    likes_list.append(likes)

                #Ricerca per numero di views di un progetto
                if str(viewsTag) in str(span):
                    views = int(re.search(r'\d+', span.get_text()).group())
                    views_list.append(views) 
            i = i + 1
                
        except rq.ConnectionError:
            time.sleep(60)
        
    return remixed_list,project_depth_list,time_list,comments_list,likes_list,views_list

#Funzione che restituisce gli autori di tutte le pagine
import re
def findAuthors():    
    authors_list = []
    print('findAuthors function started')
    repeat = True
    
    #ricerca dell'ultima pagina
    while repeat:
        try:
            url = "https://www.paneljam.com/stars/"
            page = rq.get(url)  
            soup = BeautifulSoup(page.content, 'html.parser')
            span= soup.find('span', class_ = 'last')
            page = span.find('a')
            last_page = page['href']
            last = int(re.search(r'\d+', last_page).group())
            repeat = False
        except rq.ConnectionError:
            time.sleep(60)
            
    i = 1

    #estrazione di tutti gli autori
    while i <= last:
        try:
            if i != 257:            
                url ='https://www.paneljam.com/stars/?page=' + str(i)
                page = rq.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                content = soup.find_all('a', class_='strip-preview-click')     
                for c in content:
                        print(c['href'])
                        authors_list.append(c['href'])
                i = i + 1
                
            else:
                i = i + 1  
        except rq.ConnectionError:
                time.sleep(60)
            
    authors_list = list(dict.fromkeys(authors_list))            
    return authors_list 

def shared_projects(authors_list):
    i = 0
    shared = []
    while i < len(authors_list):
        
        print('Projects of ' + authors_list[i])
        url = "https://www.paneljam.com/" + authors_list[i] + "/?page=1"
        page = rq.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        projects = soup.find('div', class_="profile__menu")
        author = projects.find('a')
        span = author.find('span')
        print(span.text)
        shared.append(span.text)
        i = i + 1
    return shared

def created_panels(authors_list):
    panels = []
    for author in authors_list:
        panels.append(authors_list.count(author))
    return panels

def findProjects():
    import re
    
    totProjects = []
    url ="https://www.paneljam.com/jams/"
    page = rq.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    wrap_group = soup.find('div', class_ = "wrap group wrap--with-sidebar")
    pagination = wrap_group.find('span', class_ = 'last')
    last = pagination.find('a')
    pages = last['href']
    pages = int(re.search(r'\d+', pages).group())
    i = 1
    while i <= pages:
        print(str(i)+" of "+str(pages)+" pages.")
        url = "https://www.paneljam.com/jams/?page="+str(i)
        page = rq.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        strip_grid = soup.find('div', class_ = "strip-grid")
        jams = strip_grid.findAll('div',class_ = 'jams-wrap')
        
        for jam in jams:
            a = jam.findAll('a',class_ = 'strip-preview-click')
            for ref in a:
                if bool(re.search(r'\d', a['href'])) is True:
                    project = ref['href']
                    project = int(re.search(r'\d+', ref['href']).group())
                    totProjects.append(project)
    
        i = i + 1
    print(totProjects)
    print(len(totProjects))
    return totProjects


#Estrazione dell'ultima pagina dei progetti svolti da un utente
    
def lovesAndViews(authors_list,shared):
    
    import re
    authors_loves = []
    authors_views = []
    totProjects = []
    i = 0

    while i < len(authors_list):
        pageCount = 0
        try:
        
            print('Projects of ' + authors_list[i])
            loves = []
            views = []
            url = "https://www.paneljam.com/"+authors_list[i]+"/?page=1"
            page = rq.get(url)
            soup = BeautifulSoup(page.content,'html.parser')
            pages = soup.find('div', class_ = "txt-center wrap load-more-wrapper")
            nav = pages.find('nav', class_ = 'pagination')
            
            if nav is None:
                last = 1
            else:
                span = nav.find('span', class_ = 'last')
                page = span.find('a')
                last_page = page['href']
                last = int(re.search(r'\d+', last_page).group())


            #Estrazione di tutti i progetti
            a = 1
            while a <= last:
                try:
                    url = "https://www.paneljam.com/"+authors_list[i]+"/?page="+str(a)
                    page1 = rq.get(url)
                    soup = BeautifulSoup(page1.content,'html.parser')
                    projects = soup.find('div', class_ = 'profile__content txt-center')
                    project_list = projects.find_all('a',class_ = 'strip-preview-click')

                    if project_list is None:
                        loves.append(0)
                        views.append(0)
                        a = a + 1
                    else:
                        counter = 0
                        
                        while counter < len(project_list):
                            try:
                                #print((project_list[counter])['href'])
                                print(str(pageCount) + " of " + str(shared[i]) + "  " + (project_list[counter])['href'])
                                pageCount = pageCount+1
                                
                                url = "https://www.paneljam.com"+(project_list[counter])['href']
                                page2 = rq.get(url)
                                soup = BeautifulSoup(page2.content,'html.parser')
                                stats_bar = soup.find('div', class_ = "action-bar")
                                stats = stats_bar.find('div',class_ = "right")
                                lovesTag = stats.find('img', alt = "Likes Count Icon")
                                viewsTag = stats.find('img',alt = "Views Count Icon")
                                spans = stats.find_all('span')

                                for span in spans:
                                    if str(lovesTag) in str(span):
                                        result = span.get_text()
                                        total_loves = int(re.search(r'\d+', result).group())
                                        loves.append(total_loves)

                                    if str(viewsTag) in str(span):
                                        result = span.get_text()
                                        total_views = int(re.search(r'\d+', result).group())
                                        views.append(total_views)
                                        
                                counter = counter + 1
                            except rq.ConnectionError:
                                time.sleep(60)
                                        
                        a = a + 1
                except rq.ConnectionError:
                    time.sleep(60)
                    
            authors_loves.append(sum(loves))
            authors_views.append(sum(views))
            i = i + 1
            
        except rq.ConnectionError:
            time.sleep(60)
    
    return authors_loves,authors_views
  