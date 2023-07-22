from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen,Request
import csv
import time
def element_scraper(driver):
    try:
        CN=WebDriverWait(driver,2).until(EC.presence_of_element_located((By.TAG_NAME,"h1"))).text
    except: 
        CN='missing'
    try:
        WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH,"//div[@class='media-body private-media__body']")))
        rating=driver.find_element(By.XPATH,"//div[@class='media-body private-media__body']").text
    except:
        rating='missing'
    try:
        WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH,"//span[@class='private-big']")))
        desc=' '.join(driver.find_element(By.XPATH,"//span[@class='private-big']").text.split('\n'))
    except:
        desc='missing'
    try:
        link=WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.XPATH,"//a[@class='private-link uiLinkWithoutUnderline uiLinkDark']")))[-1].get_attribute('href')
    except:
        link='missing'
    try:
        WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH,"//h3[@class='Heading-gv4tyh-0 H3-sc-3ussel-0 gtwmLy is--heading-5 m-bottom-2 display-inline']/following-sibling::ul")))
        driver.find_element(By.XPATH,"//button[@class='uiButton private-button private-button__link private-button--default private-expandable-text__toggle-button align-left']").click()
        slots=driver.find_elements(By.XPATH,"//h3[@class='Heading-gv4tyh-0 H3-sc-3ussel-0 gtwmLy is--heading-5 m-bottom-2 display-inline']/following-sibling::ul")
        print('\n')
        srvis=slots[0].find_elements(By.TAG_NAME,"li")
        srvs=[i.text for i in srvis]
        productss=slots[1].find_elements(By.TAG_NAME,"li")
        products=[i.text for i in productss]
    except:
        products=[]
        srvs=[]
    try:
        WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH,"//a[@class='private-link uiLinkWithoutUnderline uiLinkDark']")))
        places=driver.find_elements(By.XPATH,"//a[@class='private-link uiLinkWithoutUnderline uiLinkDark")[1:-1]
        place=[i.text for i in places]
    except:
        place='missing'

    datapoint=[CN,rating,'hubspot',place,'emplyerscount','yrfounded','missing',srvs,products,desc,'ceo','mail',link]
    return datapoint

def hubspot_links_getter(*args):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    options.add_argument("--start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--headless')

    driver = webdriver.Chrome(service=service,options=options)
    
    searchphrase=''
    if args:
        for arg in args:
            if arg!='':
                searchphrase+=arg+"%20"
        searchphrase=searchphrase[:-3]
    else: searchphrase='';print("searchphrase empty")
    
    url="https://ecosystem.hubspot.com/marketplace/solutions/page/1?eco_search="+searchphrase
   
    driver.get(url)
    print("Hubspot:")
    try:
        s=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,"//span[@class='private-big']"))).text.split(' ')[2]
    except:
        return ['no results associated with given filters']
    if len(s)>3:
        s=s[0]+s[2:]
    pages_number=int(s)//45 if int(s)%45==0 else (int(s)//45)+1
    data=[]
    for i in range(pages_number):
        print(i+1)
        try:
            WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,"//a[@class='private-link uiLinkWithoutUnderline ResultCard__StyledLink-sc-2sddbc-0 jYcurs private-link--unstyled']")))
        except:
            print("something wrong in load")
        try:
            kk=driver.find_elements(By.XPATH,"//a[@class='private-link uiLinkWithoutUnderline ResultCard__StyledLink-sc-2sddbc-0 jYcurs private-link--unstyled']")
        except:
            print("something went wrong with this page")
            continue
        for j in range(len(kk)):
            print(j,"                        ",len(kk))
            try:
                WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,"//a[@class='private-link uiLinkWithoutUnderline ResultCard__StyledLink-sc-2sddbc-0 jYcurs private-link--unstyled']")))
            except:
                print("refreshing web elements failed")
                continue
            try:
                print("tried")
                kk=driver.find_elements(By.XPATH,"//a[@class='private-link uiLinkWithoutUnderline ResultCard__StyledLink-sc-2sddbc-0 jYcurs private-link--unstyled']")
                kk[j].click()
                datta=element_scraper(driver)
                data.append(datta)
            except:
                print("refreshing web elements faileddd")
            try:
                back=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//a[@class='private-link uiLinkWithoutUnderline private-breadcrumbs__item uiLinkLight private-link--on-dark']")))
                back.click()
            except Exception:
                print(Exception)
                back=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//a[@class='private-link uiLinkWithoutUnderline private-breadcrumbs__item uiLinkLight private-link--on-dark']")))
                back.click()
                print("second time quitting")
            except:
                print("failed to go back!")
        print("scraped {0} elements ".format(len(data)))
        btn=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,"//button[@aria-label='Next page']")))
        btn.click()
    driver.quit()
    return data