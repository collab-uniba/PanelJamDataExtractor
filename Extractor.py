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
    today = date.today()
    start_time = time.time()
    printTime = time.strftime("%H:%M:%S", time.gmtime(start_time))
    print('Start date: '+ str(today) + ' ' + printTime)
    
    #Estrazione features degli autori
    authors_list = findAuthors()
    (authors_loves, authors_views, totProjects) = lovesAndViews(authors_list)
    stars_list = star_count(authors_list)
    avatars = has_avatar(authors_list)
    bios = has_bio(authors_list)
    nFollowers = followers(authors_list)
    createAuthorsTable(authors_list,stars_list,avatars,bios,nFollowers,authors_loves,authors_views)
    
    #Estrazione features dei progetti    
    (remixed_list, project_depth_list, time_list, comments_list, likes_list, views_list) = project_stats(totProjects)
    createProjectsTable(totProjects,remixed_list,likes_list,views_list,comments_list,project_depth_list,time_list)
    
    
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
    df.to_excel('TabellaProgettiPanelJam.xlsx', index = False)    
    
def createAuthorsTable(authors_list,stars_list,avatars,bios,nFollowers,authors_loves,authors_views):
    import pandas as pd
    
    data = {'Authors': authors_list,
            'Stars': stars_list,
            'Has Avatar': avatars,
            'Has Bio': bios,
            'Followers': nFollowers,
            'Tot loves': authors_loves,
            'Tot views': authors_views}
    df = pd.DataFrame(data, columns = ['Authors','Stars','Has Avatar','Has Bio','Followers','Tot loves','Tot views'])
    df.to_excel('TabellaAutoriPanelJam.xlsx', index = False)
        
#file html di un utente casuale della community
def star_count(authors_list):
    stars_list = []
    print('star_count function started')
    i = 0
    while i < len(authors_list):
        try:
            url ="https://www.paneljam.com"+authors_list[i]
            page1 = rq.get(url)
            soup = BeautifulSoup(page1.content, 'html.parser')
            
            #Ricerca per tag e class per estrapolare la feature star_count
            stars = soup.find('div', class_='star-count').get_text()
            stars_list.append(stars)
            print(stars,end='\r')
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
            url = "https://www.paneljam.com"+authors_list[i]
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
            friends_list = profile_menu.find('a',href=re.compile('/friends'))
            print(authors_list[i]+' friends: ' + friends_list.get_text())
            friends = friends_list.get_text()
            nFollowers.append(friends)
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
            
    i = 120

    #estrazione di tutti gli autori
    while i < 121:
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

#Estrazione dell'ultima pagina dei progetti svolti da un utente
def lovesAndViews(authors_list):
    
    import re
    authors_loves = []
    authors_views = []
    totProjects = []
    i = 0
    while i < len(authors_list):
        try:
        
            print('Projects of ' + authors_list[i])
            loves = []
            views = []
            url = "https://www.paneljam.com"+authors_list[i]+"?page=1"
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
                    url = "https://www.paneljam.com"+authors_list[i]+"?page="+str(a)
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
                                print((project_list[counter])['href'])
                                totProjects.append((project_list[counter])['href'])
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
            
    totProjects = list(dict.fromkeys(totProjects))     
    
    return authors_loves,authors_views,totProjects
  