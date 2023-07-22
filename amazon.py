from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

def dataweree(*args):
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
                searchphrase+=arg+", "
        searchphrase=searchphrase[:-2]
    else: searchphrase='';print("searchphrase empty")
    

    url="https://partners.amazonaws.com/search/partners"
    driver.get(url)

    search=driver.find_element(By.XPATH,"//input[@id='awsui-autosuggest-0']")

    search.send_keys(searchphrase)
    search.send_keys(Keys.RETURN)
    time.sleep(2)
    print("Amazon:")
    try:
        resnum=int(WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,"//span[@class='search-results-count']"))).text)
    except:
        return []
    pages_number=resnum//10 if resnum%10==0 else (resnum//10)+1
    print(resnum,'  ',pages_number)
    hrefs=[]
    for i in range(pages_number):
        elems=WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.XPATH,"//a[@class='partner-link card-title']")))
        page=bs(driver.page_source,"html.parser")
         
        linkos=page.find_all("a",{"class":"partner-link card-title"})[:10]
        links=[l['href'] for l in linkos]

        hrefs=hrefs+links
        next=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,"//li[@data-testid='pagination-right-arrow']")))
        next.click()
    print("Got all the products links")
    data=[]
    print("scraping elements...")
    for href in hrefs:
        url="https://partners.amazonaws.com"+href.replace(' ','%20')
        driver.get(url)
        time.sleep(1)
        page = bs(driver.page_source, "html.parser")
        try:
            CN=page.find("div",{"class":"partner-bio__header h1"}).text
        except :
            CN="missing"

        try: 
            place=page.find("address").text
        except:
            place="missing"
        
        try:
            srvs=page.find_all("p",{"class":"solution-refiners"})
            srvs=[sr.text for sr in srvs]
        except:
            srvs=['missing']

        try:
            desc=page.find("div",{"class":"split-panel__blurb"}).text
        except:
            desc=['missing']

        try:
            link=page.find("svg",{"data-icon":"external-link-alt"}).text
        except:
            link='missing'
        datapoint=[CN,'missing','Amazon',place,'missing','missing','missing',srvs,'missing',desc,'missing','missing',link]
        data.append(datapoint)

    driver.quit()
    return data