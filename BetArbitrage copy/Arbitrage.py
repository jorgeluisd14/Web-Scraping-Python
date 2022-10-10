from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class Arbitrage:
    
    def Co(M,C,N):
        for l in range(0,len(M)-1,1):

            c = l+1

            for m in range(c,len(M),1):
                        
                coin1 = []
                coin2 = []

                for k in M[l]:
                    for j in M[m]:
                        if k[0:4] in j and j[0:4] in k:
                            coin1.append(M[l].index(k)) 
                            coin2.append(M[m].index(j))

                m1 =[M[l][n] for n in coin1]
                m2 =[M[m][n] for n in coin2]
                c1 = [C[l][n] for n in coin1]
                c2 = [C[m][n] for n in coin2]
                ar1 =[1/c1[n][0]+1/c2[n][1] for n in range(len(c1))]
                ar2 =[1/c1[n][1]+1/c2[n][0]for n in range(len(c1))]

                opor_t = []
                for i,j in zip(ar1,ar2):
                    if i<1 or j<1: 
                        opor_t.append("SI")
                    else: 
                        opor_t.append("NO") 

                df = pd.DataFrame({f"MATCH1 {N[l]}":m1,f"MATCH2 {N[m]}":m2,"CUOTE_1":c1,"CUOTE_2":c2,"AR1":ar1,"AR2":ar2,"OPORTUNIDAD":opor_t})
                print(df)


    def Tennis():
        url_bwin = 'https://sports.bwin.co/es/sports/tenis-5/apuestas'
        path = '/Users/jorgedavidmesa/Desktop/chromedriver'

        driver = webdriver.Chrome(path)

        driver.get(url_bwin)
        driver.delete_all_cookies()
        driver.set_window_size(800, 1080)
        time.sleep(2)
        bot = driver.find_element(By.XPATH,'//i[@class="theme-sorting"]')
        bot.click()
        time.sleep(0.5)
        bot2 = driver.find_element(By.XPATH,'//div[@class="sort-selector-option"]')
        bot2.click()
        time.sleep(2)
        bot3 = driver.find_elements(By.XPATH,'//div[@class="header-wrapper ng-star-inserted"]')
        for i in bot3:
            i.click()
        time.sleep(0.5) 
        bot3[-1].click() 
        time.sleep(2.5)  
            
        matches = driver.find_elements(By.TAG_NAME,'ms-event-name')
        driver.execute_script("arguments[0].scrollIntoView();", matches[-1]) 
        time.sleep(2.5)
        
        if len(driver.find_elements(By.TAG_NAME,'ms-event-name')) == 0:
         bot31 = driver.find_elements(By.XPATH,'//div[@class="header-wrapper ng-star-inserted"]')
         bot31[-1].click() 
         time.sleep(2)
        else:
         try:      
             driver.find_element(By.XPATH,'//div[@class="grid-footer ms-active-highlight ng-star-inserted"]').click()
             time.sleep(2)
         except:
             pass    


        matches = driver.find_elements(By.TAG_NAME,'ms-event-name')
        cuotes = driver.find_elements(By.TAG_NAME,'ms-option-group')

        m_tennis_bwin = [match.text for match in matches]
        c_bwin = [cuot.text for cuot in cuotes]

        driver.quit()

        for i in range(len(m_tennis_bwin)):
            m_tennis_bwin[i] = m_tennis_bwin[i].upper()
            m_tennis_bwin[i] = re.sub(r"\n"," ",m_tennis_bwin[i])


        iso = pd.read_csv('paises.csv')
        iso = list(iso[' iso3'])
        for j in range(len(iso)):
            iso[j] = iso[j] + " "

        for i in range(len(m_tennis_bwin)):
            m_tennis_bwin[i] = m_tennis_bwin[i]+" "
            for j in iso:
                m_tennis_bwin[i]=(re.sub(j," ",m_tennis_bwin[i]))

        for i in range(len(c_bwin)):
            c_bwin[i] = c_bwin[i].upper()
            c_bwin[i] = re.sub(r"\n"," ",c_bwin[i])

        c_bwin_tennis1 = " ".join(c_bwin).split(" ")
        c_tennis_bwin=[]
        
        n = len(c_bwin_tennis1)

        for i in range(1,n,2):
            if c_bwin_tennis1[i]=='':
                c_bwin_tennis1[i] = '0'
            if c_bwin_tennis1[i-1]=='':
                c_bwin_tennis1[i-1] = '0'  
                
            c_tennis_bwin.append([float(c_bwin_tennis1[i-1]),float(c_bwin_tennis1[i])])


        page_w  = requests.get("https://apuestas.wplay.co/es/s/TENN/Tenis")
        soup_w = BeautifulSoup(page_w.content, 'html.parser')
        soup_w=soup_w.prettify().split("Próximas Apuestas de Tenis")
        soup_w=BeautifulSoup(soup_w[1],'html.parser')
        price_w=soup_w.select(r'span.price')
        name_w = soup_w.select(r'span.seln-name')
        name_w=[a.get_text() for a in name_w]
        for i in range(len(name_w)):
            name_w[i] = re.sub(r"\n\s+ | \s+","",name_w[i])
        price_w=[a.get_text() for a in price_w]
        price_w = ''.join(price_w)
        price_w=re.findall("\d+\.\d\d",price_w)

        n = len(name_w)
        m_tennis_wplay=[name_w[i].upper()+' '+name_w[i+1].upper() for i in range(0,n,2)]
        
        n = len(price_w)
        c_tennis_wplay=[[float(price_w[i-1]),float(price_w[i])] for i in range(1,n,2)]
        


        url3 = 'https://www.rushbet.co/?page=sportsbook#filter/tennis'
        path = '/Users/jorgedavidmesa/Desktop/chromedriver'

        driver = webdriver.Chrome(path)

        driver.get(url3)
        driver.maximize_window()
        driver.delete_all_cookies()
        time.sleep(5)

        bot = driver.find_element(By.XPATH,'//header[@data-touch-feedback="true"]')
        bot.click()
        bot2 = driver.find_element(By.XPATH,'//li[@data-id="sortByTime"]')
        bot2.click()
        time.sleep(2)  

        bot3 = driver.find_elements(By.XPATH,'//header[@class="CollapsibleContainer__HeaderWrapper-sc-1bmcohu-1 ejjRFS"]')
        for i in bot3:
            i.click() 
        time.sleep(1)  
        bot4 = driver.find_elements(By.XPATH,'//header[@class="CollapsibleContainer__HeaderWrapper-sc-1bmcohu-1 AZXzA"]')
        bot4[1].click()

        n = driver.find_elements(By.XPATH,'//header[@class="CollapsibleContainer__HeaderWrapper-sc-1bmcohu-1 hqPeYh"]') 
        for i in n:
            i.click() 
        
        bot4 = driver.find_elements(By.CLASS_NAME,"KambiBC-event-participants__name")

        mt_rush = []

        for i in bot4:
            mt_rush.append(i.text)

        bot5 = driver.find_elements(By.XPATH,'//div[@class="OutcomeButton__Odds-sc-1anyy32-5 gfVAbN"]')

        ct_rush = []

        for i in bot5:
            ct_rush.append(i.text)

        time.sleep(2) 
        driver.quit()

        m_tennis_rush=[]
        n = len(mt_rush)
        for i in range(0,n,2):
            m_tennis_rush.append(mt_rush[i].upper()+' '+mt_rush[i+1].upper())
            
        m_tennis_rush=list(map(lambda x:re.sub(",","",x),m_tennis_rush))

        c_tennis_rush=[]
        n = len(ct_rush)
        for i in range(0,n,2):
            c_tennis_rush.append([float(ct_rush[i]),float(ct_rush[i+1])])



        url_zamba = "https://www.zamba.co/es/apuestas-deportivas/deportes/848"
        path = '/Users/jorgedavidmesa/Desktop/chromedriver'

        driver = webdriver.Chrome(path)
        driver.get(url_zamba)
        driver.delete_all_cookies()
        driver.set_window_size(500, 1080)
        time.sleep(10)

        try:
            bot1 = driver.find_element(By.XPATH,'//button[@class="g1-button secondary negative"]')
            driver.execute_script("arguments[0].scrollIntoView();", bot1)
            time.sleep(4)
            bot1.click()
        except:
            pass    

        bot2 = driver.find_elements(By.CLASS_NAME,'text')
        m_zamba = [match.text for match in bot2]

        bot3 = driver.find_elements(By.CLASS_NAME,'odd')
        c_zamba = [cuote.text for cuote in bot3]
        time.sleep(1)

        driver.quit() 

        def j(x):
            if len(re.findall("",x)) == 1:
                return 0.01
            else:
                return x

        c_zamba = list(map(j, c_zamba))
        
        m_zamba2 = [re.sub(r"Ganado.+|Total.+|\d.+","",m_zamba[i]) for i in range(len(m_zamba))]

        while(True):
         try:   
             m_zamba2.remove("")
         except:
             break 

        m_tennis_zamba = [m_zamba2[i-1].upper()+" "+m_zamba2[i].upper() for i in range(1,len(m_zamba2),2)]
        c_tennis_zamba = [[float(c_zamba[i-1]),float(c_zamba[i])] for i in range(1,len(c_zamba),2)]
   
        M_tennis = [m_tennis_bwin,m_tennis_rush,m_tennis_wplay,m_tennis_zamba]
        C_tennis = [c_tennis_bwin,c_tennis_rush,c_tennis_wplay,c_tennis_zamba]
        M_tennis2 = ["bwin","rush","wplay","zamba"] 

        Arbitrage.Co(M_tennis,C_tennis,M_tennis2)        


    def TableTennis(): 

        url_bwin = 'https://sports.bwin.co/es/sports/tenis-de-mesa-56/apuestas'
        path = '/Users/jorgedavidmesa/Desktop/chromedriver'

        driver = webdriver.Chrome(path)

        driver.get(url_bwin)
        driver.delete_all_cookies()
        driver.set_window_size(800, 1080)
        time.sleep(2)
        bot = driver.find_element(By.XPATH,'//i[@class="theme-sorting"]')
        bot.click()
        time.sleep(0.5)
        bot2 = driver.find_element(By.XPATH,'//div[@class="sort-selector-option"]')
        bot2.click()
        time.sleep(2)
        bot3 = driver.find_elements(By.XPATH,'//div[@class="header-wrapper ng-star-inserted"]')
        for i in bot3:
            i.click()
        time.sleep(0.5) 
        bot3[-1].click() 
        time.sleep(2.5)  
            
        matches = driver.find_elements(By.TAG_NAME,'ms-event-name')
        driver.execute_script("arguments[0].scrollIntoView();", matches[-1]) 
        time.sleep(2.5)

        if len(driver.find_elements(By.TAG_NAME,'ms-event-name')) == 0:
         bot31 = driver.find_elements(By.XPATH,'//div[@class="header-wrapper ng-star-inserted"]')
         bot31[-1].click() 
         time.sleep(2)
        else:
         try:      
             driver.find_element(By.XPATH,'//div[@class="grid-footer ms-active-highlight ng-star-inserted"]').click()
             time.sleep(2)
         except:
             pass  

        matches = driver.find_elements(By.TAG_NAME,'ms-event-name')
        cuotes = driver.find_elements(By.TAG_NAME,'ms-option-group')


        m_tablet_bwin = [match.text for match in matches]
        c_bwin = [cuot.text for cuot in cuotes]

        driver.quit()

        for i in range(len(m_tablet_bwin)):
            m_tablet_bwin[i] = m_tablet_bwin[i].upper()
            m_tablet_bwin[i] = re.sub(r"\n"," ",m_tablet_bwin[i])


        iso = pd.read_csv('paises.csv')
        iso = list(iso[' iso3'])
        for j in range(len(iso)):
         iso[j] = iso[j] + " "

        for i in range(len(m_tablet_bwin)):
            m_tablet_bwin[i] = m_tablet_bwin[i]+" "
            for j in iso:
             m_tablet_bwin[i]=(re.sub(j," ",m_tablet_bwin[i]))

        for i in range(len(c_bwin)):
            c_bwin[i] = c_bwin[i].upper()
            c_bwin[i] = re.sub(r"\n"," ",c_bwin[i])

        cuo_tabletbwin = " ".join(c_bwin).split(" ")

        c_tablet_bwin=[]
        n = len(cuo_tabletbwin)

        for i in range(1,n,2):
            if cuo_tabletbwin[i]=='':
                cuo_tabletbwin[i] = '0'
            if cuo_tabletbwin[i-1]=='':
                cuo_tabletbwin[i-1] = '0'       
            c_tablet_bwin.append([float(cuo_tabletbwin[i-1]),float(cuo_tabletbwin[i])])

        
        page_w  = requests.get("https://apuestas.wplay.co/es/s/TABL/Tenis-de-Mesa")
        soup_w = BeautifulSoup(page_w.content, 'html.parser')
        soup_w=soup_w.prettify().split("Próximas Apuestas de Tenis de Mesa")
        soup_w=BeautifulSoup(soup_w[1],'html.parser')
        price_w=soup_w.select(r'span.price')
        name_w = soup_w.select(r'span.seln-name')
        name_w=[a.get_text() for a in name_w]
        for i in range(len(name_w)):
            name_w[i] = re.sub(r"\n\s+ | \s+","",name_w[i])
        price_w=[a.get_text() for a in price_w]
        price_w = ''.join(price_w)
        price_w=re.findall("\d+\.\d\d",price_w)

        m_tablet_wplay=[]
        n = len(name_w)

        for i in range(1,n,2):
            m_tablet_wplay.append(name_w[i-1].upper()+' '+name_w[i].upper())

        c_tablet_wplay=[]
        n = len(price_w)
        for i in range(1,n,2):
            c_tablet_wplay.append([float(price_w[i-1]),float(price_w[i])])



        url3 = 'https://www.rushbet.co/?page=sportsbook#filter/table_tennis'
        path = '/Users/jorgedavidmesa/Desktop/chromedriver'

        driver = webdriver.Chrome(path)

        driver.get(url3)
        driver.maximize_window()
        driver.delete_all_cookies()
        time.sleep(2)

        bot = driver.find_element(By.XPATH,'//header[@data-touch-feedback="true"]')
        bot.click()
        bot2 = driver.find_element(By.XPATH,'//li[@data-id="sortByTime"]')
        bot2.click()
        time.sleep(2)  

        bot3 = driver.find_elements(By.XPATH,'//header[@class="CollapsibleContainer__HeaderWrapper-sc-1bmcohu-1 ejjRFS"]')
        for i in bot3:
            i.click() 
        time.sleep(1)  
        bot4 = driver.find_elements(By.XPATH,'//header[@class="CollapsibleContainer__HeaderWrapper-sc-1bmcohu-1 AZXzA"]')
        bot4[-1].click()

        n = driver.find_elements(By.XPATH,'//header[@class="CollapsibleContainer__HeaderWrapper-sc-1bmcohu-1 hqPeYh"]') 
        for i in n:
            i.click() 
        
        bot4 = driver.find_elements(By.CLASS_NAME,"KambiBC-event-participants__name")

        mt_rush = []

        for i in bot4:
            mt_rush.append(i.text)

        bot5 = driver.find_elements(By.XPATH,'//div[@class="OutcomeButton__Odds-sc-1anyy32-5 gfVAbN"]')

        ct_rush = []

        for i in bot5:
            ct_rush.append(i.text)

        time.sleep(2) 
        driver.quit()

        mt_rush2=[]
        n = len(mt_rush)
        for i in range(0,n,2):
            mt_rush2.append(mt_rush[i].upper()+' '+mt_rush[i+1].upper())
            
        m_tablet_rush=list(map(lambda x:re.sub(",","",x),mt_rush2))
   

        c_tablet_rush=[]
        n = len(ct_rush)
        for i in range(0,n,2):
            c_tablet_rush.append([float(ct_rush[i]),float(ct_rush[i+1])]) 



        url_zamba = "https://www.zamba.co/es/apuestas-deportivas/deportes/884"
        path = '/Users/jorgedavidmesa/Desktop/chromedriver'

        driver = webdriver.Chrome(path)

        driver.get(url_zamba)
        driver.delete_all_cookies()
        time.sleep(8)

        try:
            bot1 = driver.find_element(By.XPATH,'//button[@class="g1-button secondary negative"]')
            driver.execute_script("arguments[0].scrollIntoView();", bot1)
            time.sleep(4)
            bot1.click()
        except:
            pass    

        bot2 = driver.find_elements(By.CLASS_NAME,'text')
        m_zamba = []

        for match in bot2:
            m_zamba.append(match.text)

        c_zamba = []

        bot3 = driver.find_elements(By.CLASS_NAME,'odd')

        for cuote in bot3:
            c_zamba.append(cuote.text)

        time.sleep(2)

        driver.quit() 

        while(True):
            try:   
                m_zamba.remove("")
            except:
                break  

        m_tablet_zamba = [m_zamba[i-1].upper()+" "+m_zamba[i].upper() for i in range(1,len(m_zamba),2)]
        c_tablet_zamba = [[float(c_zamba[i-1]),float(c_zamba[i])] for i in range(1,len(c_zamba),2)]

        M_tablet = [m_tablet_bwin,m_tablet_rush,m_tablet_wplay,m_tablet_zamba]
        C_tablet = [c_tablet_bwin,c_tablet_rush,c_tablet_wplay,c_tablet_zamba]
        N_tablet = ["BWIN","RUSH","WPLAY","ZAMBA"]  
        Arbitrage.Co(M_tablet,C_tablet,N_tablet)

    def Volley():

        url_bwin = 'https://sports.bwin.co/es/sports/voleibol-18/apuestas'
        path = '/Users/jorgedavidmesa/Desktop/chromedriver'

        driver = webdriver.Chrome(path)

        driver.get(url_bwin)
        driver.delete_all_cookies()
        driver.set_window_size(800, 1080)
        time.sleep(2)
        bot = driver.find_element(By.XPATH,'//i[@class="theme-sorting"]')
        bot.click()
        time.sleep(0.5)

        bot2 = driver.find_element(By.XPATH,'//div[@class="sort-selector-option"]')
        bot2.click()
        time.sleep(2)

        bot3 = driver.find_elements(By.XPATH,'//div[@class="header-wrapper ng-star-inserted"]')
        for i in bot3:
            i.click()
        time.sleep(0.5) 
        bot3[1].click() 
        time.sleep(2)  
            
        matches = driver.find_elements(By.TAG_NAME,'ms-event-name')
        driver.execute_script("arguments[0].scrollIntoView();", matches[-1]) 
        time.sleep(2)

        if len(driver.find_elements(By.TAG_NAME,'ms-event-name')) == 0:
         bot31 = driver.find_elements(By.XPATH,'//div[@class="header-wrapper ng-star-inserted"]')
         bot31[-1].click() 
         time.sleep(2)
        else:
         try:      
             driver.find_element(By.XPATH,'//div[@class="grid-footer ms-active-highlight ng-star-inserted"]').click()
             time.sleep(2)
         except:
             pass    


        matches = driver.find_elements(By.TAG_NAME,'ms-event-name')
        cuotes = driver.find_elements(By.TAG_NAME,'ms-option-group')


        m_volley_bwin = []

        for match in matches:
            m_volley_bwin.append(match.text)

        c_bwin = []

        for cuot in cuotes:
            c_bwin.append(cuot.text)

        driver.quit()

        for i in range(len(m_volley_bwin)):
            m_volley_bwin[i] = m_volley_bwin[i].upper()
            m_volley_bwin[i] = re.sub(r"\n"," ",m_volley_bwin[i])


        iso = pd.read_csv('paises.csv')
        iso = list(iso[' iso3'])
        for j in range(len(iso)):
            iso[j] = iso[j] + " "

        for i in range(len(m_volley_bwin)):
            m_volley_bwin[i] = m_volley_bwin[i]+" "
            for j in iso:
                m_volley_bwin[i]=(re.sub(j," ",m_volley_bwin[i]))

        for i in range(len(c_bwin)):
            c_bwin[i] = c_bwin[i].upper()
            c_bwin[i] = re.sub(r"\n"," ",c_bwin[i])


        CUO = " ".join(c_bwin).split(" ")

        c_volley_bwin=[]
        n = len(CUO)

        for i in range(1,n,2):
            if CUO[i]=='':
                CUO[i] = '0'
            if CUO[i-1]=='':
                CUO[i-1] = '0'  
                
            c_volley_bwin.append([float(CUO[i-1]),float(CUO[i])])



        page_w  = requests.get("https://apuestas.wplay.co/es/s/VOLL/Voleibol")
        soup_w = BeautifulSoup(page_w.content, 'html.parser')
        soup_w=soup_w.prettify().split("Próximas Apuestas de Voleibol")
        soup_w=BeautifulSoup(soup_w[1],'html.parser')
        price_w=soup_w.select(r'span.price')
        name_w = soup_w.select(r'span.seln-name')
        name_w=[a.get_text() for a in name_w]
        for i in range(len(name_w)):
            name_w[i] = re.sub(r"\n\s+ | \s+","",name_w[i])
        price_w=[a.get_text() for a in price_w]
        price_w = ''.join(price_w)
        price_w=re.findall("\d+\.\d\d",price_w)

        m_volley_wplay=[]
        n = len(name_w)

        for i in range(1,n,2):
            m_volley_wplay.append(name_w[i-1].upper()+' '+name_w[i].upper())

        c_volley_wplay=[]
        n = len(price_w)
        for i in range(1,n,2):
            c_volley_wplay.append([float(price_w[i-1]),float(price_w[i])])


        url3 = 'https://www.rushbet.co/?page=sportsbook#filter/volleyball'
        path = '/Users/jorgedavidmesa/Desktop/chromedriver'

        driver = webdriver.Chrome(path)

        driver.get(url3)
        driver.maximize_window()
        driver.delete_all_cookies()
        time.sleep(2)

        bot = driver.find_element(By.XPATH,'//header[@data-touch-feedback="true"]')
        bot.click()
        bot2 = driver.find_element(By.XPATH,'//li[@data-id="sortByTime"]')
        bot2.click()
        time.sleep(2)  

        bot3 = driver.find_elements(By.XPATH,'//header[@class="CollapsibleContainer__HeaderWrapper-sc-1bmcohu-1 ejjRFS"]')
        for i in bot3:
            i.click() 
        time.sleep(1)  
        bot4 = driver.find_elements(By.XPATH,'//header[@class="CollapsibleContainer__HeaderWrapper-sc-1bmcohu-1 AZXzA"]')
        bot4[-1].click()

        n = driver.find_elements(By.XPATH,'//header[@class="CollapsibleContainer__HeaderWrapper-sc-1bmcohu-1 hqPeYh"]') 
        for i in n:
            i.click() 
        
        bot4 = driver.find_elements(By.CLASS_NAME,"KambiBC-event-participants__name")

        mt_rush = []

        for i in bot4:
            mt_rush.append(i.text)

        bot5 = driver.find_elements(By.XPATH,'//div[@class="OutcomeButton__Odds-sc-1anyy32-5 gfVAbN"]')

        ct_rush = []

        for i in bot5:
            ct_rush.append(i.text)

        time.sleep(2) 
        driver.quit()

        mt_rush2=[]
        n = len(mt_rush)
        for i in range(0,n,2):
            mt_rush2.append(mt_rush[i].upper()+' '+mt_rush[i+1].upper())
            
        m_volley_rush=list(map(lambda x:re.sub(",","",x),mt_rush2))

        c_volley_rush=[]
        n = len(ct_rush)
        for i in range(0,n,2):
            c_volley_rush.append([float(ct_rush[i]),float(ct_rush[i+1])])




        url_zamba = "https://www.zamba.co/es/apuestas-deportivas/deportes/852"
        path = '/Users/jorgedavidmesa/Desktop/chromedriver'

        driver = webdriver.Chrome(path)

        driver.get(url_zamba)
        driver.delete_all_cookies()
        driver.set_window_size(500, 1080)
        time.sleep(8)

        try:
            bot1 = driver.find_element(By.XPATH,'//button[@class="g1-button secondary negative"]')
            driver.execute_script("arguments[0].scrollIntoView();", bot1)
            time.sleep(4)
            bot1.click()
        except:
            pass    

        bot2 = driver.find_elements(By.CLASS_NAME,'text')
        m_zamba = []

        for match in bot2:
            m_zamba.append(match.text)

        c_zamba = []

        bot3 = driver.find_elements(By.CLASS_NAME,'odd')
        for cuote in bot3:
            c_zamba.append(cuote.text)

        time.sleep(2)

        driver.quit()



        m_zamba2 = [re.sub(r"Ganado.+|Total.+|\d.+|Live|Deportes|Otros|Favoritos|DEPORTES","",m_zamba[i]) for i in range(len(m_zamba))]

        while(True):
            try:   
                m_zamba2.remove("")
            except:
                break  

        m_volley_zamba = [m_zamba2[i-1].upper()+" "+m_zamba2[i].upper() for i in range(1,len(m_zamba2),2)]
        c_volley_zamba = [[float(c_zamba[i-1]),float(c_zamba[i])] for i in range(1,len(c_zamba),2)] 

        M_volley = [m_volley_bwin,m_volley_rush,m_volley_wplay,m_volley_zamba]
        C_volley = [c_volley_bwin,c_volley_rush,c_volley_wplay,c_volley_zamba] 
        N_volley = ["BWIN","RUSH","WPLAY","ZAMBA"]  
        Arbitrage.Co(M_volley,C_volley,N_volley)

    def Futbol():
        url_bwin2 = 'https://sports.bwin.co/es/sports/f%C3%BAtbol-4/ma%C3%B1ana'
        path = '/Users/jorgedavidmesa/Desktop/chromedriver'

        driver = webdriver.Chrome(path)

        driver.get(url_bwin2)
        driver.delete_all_cookies()
        time.sleep(10)
        bot = driver.find_element(By.XPATH,'//ms-sort-selector[@class="grid-sort-selector"]')
        bot.click()
        time.sleep(0.5)
        bot2 = driver.find_element(By.XPATH,'//div[@class="sort-selector-option"]')
        bot2.click()
        time.sleep(2)
        matchesf = driver.find_elements(By.TAG_NAME,'ms-event-name')

        mf_bwin = []
        for match in matchesf:
            mf_bwin.append(match.text)

        bot3 = driver.find_elements(By.XPATH,'//a[@class="grid-info-wrapper"]')

        t2_bwin = []

        for i in range(len(bot3)):
            bot3 = driver.find_elements(By.XPATH,'//a[@class="grid-info-wrapper"]')
            time.sleep(1)
            driver.execute_script("arguments[0].scrollIntoView();", bot3[i])
            time.sleep(1)
            bot3[i].click()
            time.sleep(2)
            try:
                bot4 = driver.find_element(By.XPATH,'//ms-over-under-option-group[@class="ng-star-inserted"]')
                t2_bwin.append(bot4.text)
            except:
                t2_bwin.append('0.0')    
            driver.back()
            time.sleep(2)
        
        driver.quit()

        def M(x):
            x = re.sub("\n"," ",x)
            x = x.upper()
            return x

        m_futbol_bwin = list(map(M,mf_bwin)) 

        c_futbol_bwin = list(map(lambda x:re.sub("\n|Mostrar más"," ",x),t2_bwin)) 

        def mas(x):
            x = re.findall(r"\b\d+\.\d\b",x)
            x = list(map(lambda y: float(y),x))
            return x
        
        def cuotes_mas(x):
            x = re.findall(r"\b\d+\.\d\d\b",x)
            x = list(map(lambda y: float(y),x))
            return x

        mas_futbol_bwin = list(map(cuotes_mas,c_futbol_bwin))
        cmas_futbol_bwin = list(map(mas,c_futbol_bwin))


        url_zamba = "https://www.zamba.co/es/apuestas-deportivas/deportes/844"
        path = '/Users/jorgedavidmesa/Desktop/chromedriver'

        driver = webdriver.Chrome(path)

        driver.get(url_zamba)
        driver.delete_all_cookies()
        driver.maximize_window()
        time.sleep(10)

        bot1 = driver.find_elements(By.XPATH,'//div[@title="mercados"]')
        m_futbol_zamba = []
        mas_futbol_zamba = []
        cmas_futbol_zamba = []

        for i in range(len(bot1)):
            bot1 = driver.find_elements(By.XPATH,'//div[@title="mercados"]')
            driver.execute_script("arguments[0].scrollIntoView();", bot1[i])
            time.sleep(1)
            bot1[i].click()
            time.sleep(5)
            bot2 = driver.find_elements(By.XPATH,'//div[@class="bet-outcome event-detail"]')
            c_zamba_futbol = [cuote.text for cuote in bot2]
            m_futbol_zamba.append(re.findall(r"\b.+\b",c_zamba_futbol[-1])[0].upper()+" "+re.findall(r"\b.+\b",c_zamba_futbol[-2])[0].upper())
            c_zamba_futbol2 = list(map(lambda x:re.findall(r"Menos de.+|Más de.+|Mas de.+",x),map(lambda x:re.sub(r"\n"," ",x),c_zamba_futbol)))
            
            while(True):
                try:   
                    c_zamba_futbol2.remove([])
                except:
                    break  
            
            mas_futbol_zamba.append(list(pd.unique(list(map(lambda x:float(re.findall(r"\d\.\d|\d",x[0])[0]),c_zamba_futbol2)))))
            cmas_futbol_zamba.append(list(map(lambda x:float(re.findall(r"\d\.\d\d",x[0])[0]),c_zamba_futbol2)))
            driver.back()
            time.sleep(5)

        driver.quit()

    


    def Esports():

        url3 = 'https://www.rushbet.co/?page=sportsbook#filter/esports'
        path = '/Users/jorgedavidmesa/Desktop/chromedriver'

        driver = webdriver.Chrome(path)

        driver.get(url3)
        driver.maximize_window()
        driver.delete_all_cookies()
        time.sleep(2)

        bot = driver.find_element(By.XPATH,'//header[@data-touch-feedback="true"]')
        bot.click()
        bot2 = driver.find_element(By.XPATH,'//li[@data-id="sortByTime"]')
        bot2.click()
        time.sleep(2)  

        bot3 = driver.find_elements(By.XPATH,'//header[@class="CollapsibleContainer__HeaderWrapper-sc-1bmcohu-1 ejjRFS"]')
        for i in bot3:
            i.click() 
        time.sleep(1)  
        bot4 = driver.find_elements(By.XPATH,'//header[@class="CollapsibleContainer__HeaderWrapper-sc-1bmcohu-1 AZXzA"]')
        bot4[2].click()

        n = driver.find_elements(By.XPATH,'//header[@class="CollapsibleContainer__HeaderWrapper-sc-1bmcohu-1 hqPeYh"]') 
        for i in n:
            i.click() 
        
        bot4 = driver.find_elements(By.CLASS_NAME,"KambiBC-event-participants__name")

        mt_rush = []

        for i in bot4:
            mt_rush.append(i.text)

        bot5 = driver.find_elements(By.XPATH,'//div[@class="OutcomeButton__Odds-sc-1anyy32-5 gfVAbN"]')

        ct_rush = []

        for i in bot5:
            ct_rush.append(i.text)

        time.sleep(2) 
        driver.quit()

        mt_rush2=[]
        n = len(mt_rush)
        for i in range(0,n,2):
            mt_rush2.append(mt_rush[i].upper()+' '+mt_rush[i+1].upper())
            
        m_esports_rush=list(map(lambda x:re.sub(",","",x),mt_rush2))

        c_esports_rush=[]
        n = len(ct_rush)
        for i in range(0,n,2):
            c_esports_rush.append([float(ct_rush[i]),float(ct_rush[i+1])])




        url_zamba = "https://www.zamba.co/es/apuestas-deportivas/deportes/169825667"
        path = '/Users/jorgedavidmesa/Desktop/chromedriver'

        driver = webdriver.Chrome(path)

        driver.get(url_zamba)
        driver.delete_all_cookies()
        driver.set_window_size(500, 1080)
        time.sleep(8)

        try:
            bot1 = driver.find_element(By.XPATH,'//button[@class="g1-button secondary negative"]')
            driver.execute_script("arguments[0].scrollIntoView();", bot1)
            time.sleep(4)
            bot1.click()
        except:
            pass    

        bot2 = driver.find_elements(By.CLASS_NAME,'text')
        m_zamba = []

        for match in bot2:
            m_zamba.append(match.text)

        c_zamba = []

        bot3 = driver.find_elements(By.CLASS_NAME,'odd')
        for cuote in bot3:
            c_zamba.append(cuote.text)

        time.sleep(2)

        driver.quit()



        m_zamba2 = [re.sub(r"Ganado.+|Total.+|\d.+|Live|Deportes|Otros|Favoritos|DEPORTES","",m_zamba[i]) for i in range(len(m_zamba))]

        while(True):
            try:   
                m_zamba2.remove("")
            except:
                break  

        m_esports_zamba = [m_zamba2[i-1].upper()+" "+m_zamba2[i].upper() for i in range(1,len(m_zamba2),2)]
        c_esports_zamba = [[float(c_zamba[i-1]),float(c_zamba[i])] for i in range(1,len(c_zamba),2)] 

        M_esports = [m_esports_rush,m_esports_zamba]
        C_esports = [c_esports_rush,c_esports_zamba]           

        for i,j in zip(M_esports,C_esports):
            print(i)
            print(j)

    def All():
        Arbitrage.Tennis()
        Arbitrage.Volley()   
        Arbitrage.TableTennis()
              