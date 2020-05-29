# -*- coding: utf-8 -*-
"""
Created on Thu May 28 16:19:25 2020

@author: utente
"""

def panelsStar():
    
    from http.cookiejar import LWPCookieJar
    import mechanize
    from bs4 import BeautifulSoup as bs
    import pandas as pd
    
    
    br = mechanize.Browser()
    
    
    cj = LWPCookieJar()
    br.set_cookiejar(cj)
    
    
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36')]
    
    br.open('https://www.paneljam.com/users/sign_in/')
    
    
   # for f in br.forms():
   #     print(f)
    
    br.select_form(nr=0)
    
    br.form['user[email]'] = 'checco640@gmail.com'
    br.form['user[password]'] = 'Checco98-'
    
    
    br.submit()
    table = pd.read_excel('..\\data\\TabellaCompleta.xlsx',index = False)
    table = table.sort_values('id_panel', ascending = True)
    idProg = table['id_prog'].tolist()
    idProg = list(dict.fromkeys(idProg))
    
    count = 0
    stars = []
    import re
    for prog in idProg:   
        print(str(count+1) +'/'+ str(len(idProg)))
        homepage = br.open('https://www.paneljam.com/jams/' + str(prog) + '/panels').read()
        homepage = bs(homepage,'html.parser')
        panel_wrap = homepage.find_all('div', class_ = 'panel-wrap')
        rows = table.loc[table['id_prog'] == prog]
        nRows = max(rows['project_depth'])
        print(nRows)
        index = 0
        for panel in panel_wrap:
            if index != nRows:
                span = panel.find('span', class_ = 'star')
                star = int(re.search(r'\d+', span.text).group())
                stars.append(star)
            else:
                break
            index = index + 1
        count = count + 1
        
    table['panel_stars'] = stars
    table.to_excel('..\\data\\TabellaCompletaProva.xlsx',index = False)
    return table