from lib2to3.pgen2 import driver
from xml.etree.ElementPath import xpath_tokenizer
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time


def scraper():
    for i in range(1,26):
        driver.get(f'https://addit3d.bilbaoexhibitioncentre.com/en/exhibitor-directory/?pagenum={i}&num_elem=25&destino=expositores&idioma=US&tab=expositores&buscar=0&certamenLov0=&certamenLov1=&certamenLov2=')
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source,features='lxml')
        table = soup.find('tbody').find_all('tr')
        all_links=[]
        for tr in table:
            d= tr.find('td')
            for link in d:
                ln = link.get('href')
                print(len(ln))
                tepm={
                    'Links':ln
                }
                all_links.append(tepm)
                df =pd.DataFrame(all_links)
                df.to_csv('link.csv')
def data_scraper():
    
    df = pd.read_csv('link.csv')
    links = df['Links'].values
    all_data = []

    for link in links:
        driver.get(link)
        time.sleep(3)

        stand = ''
        all_d=''
        interest_cntry = ''
        logo=''
        description=''
        visiting_sector=''
        
        try:
            stand = driver.find_element(By.XPATH,
                '//*[@id="tabs-1"]//div[1]/h4').text
        except:
            stand = 'None'          
        try:
            logo = driver.find_element(By.XPATH,'//*[@id="tabs-1"]/div[1]/div[1]/img').get_attribute('src')
            logo_F = str('https://app.bilbaoexhibitioncentre.com'+logo)
        except:
            pass    
        
        all_d = driver.find_element(By.XPATH,'//*[@id="tabs-1"]/div[1]/div[1]/div/p').text
        print(all_d)
        description = driver.find_element(By.XPATH,'//*[@id="tabs-1"]/div[2]').text

        try:
            visiting_sector = driver.find_element(By.XPATH,'//*[@id="tabs-1"]/div[3]/ul').text
        except:
            pass

        try:
            interest_cntry = driver.find_element('//*[@id="tabs-1"]/div[4]/ul').text
        except:
            pass    

        data_dict = {
            'Stand':stand,
            'Company Logo':logo,
            'Description':description,
            'Visiting_Sector':visiting_sector,
            'Countries Interest':interest_cntry

        }     
        all_data.append(data_dict)
        df = pd.DataFrame(all_data)
        df.to_csv('Appbilb.csv')

if __name__=='__main__': 
    driver = webdriver.Chrome(executable_path='C:/chromedriver.exe')
    # scraper()    
    data_scraper()