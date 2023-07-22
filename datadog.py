from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import random

import time

# cookies = {'name': 'sfdc-stream', 'value': '!j0GLcGK7wYG++CXogZ8dL+d/8x+VcSb76M28Hp+RWWi8+FJdvIA0p9bCLMf2qs4PC9y79j93lCQeDbs=','domain':'partners.datadoghq.com'}
# driver.add_cookie(cookies)

def datadog_UIDS_getter(*args):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    options.add_argument("--start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=service,options=options)
    driver.get("https://partners.datadoghq.com/s/PartnerDirectory")


    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,"//input[@type='search']")))
    # print("warning: ",warning,'\n',driver.find_element(By.XPATH,"//input[@type='search']"))
    time.sleep(2)
    searchbar=driver.find_element(By.XPATH,"//div[@id='myDropdown-11']").find_element(By.TAG_NAME,"input")
    # print(searchbar,'hh')

    #preparing the seach query
    searchphrase=''
    for arg in args:
        if arg:
            searchphrase+=arg+", "
    searchphrase=searchphrase[:-2]

    #searching filters
    searchbar.send_keys(searchphrase)
    btn = driver.find_element(By.XPATH, "//div[contains(@class, 'search-button')]").find_element(By.TAG_NAME,"button")
    btn.click()

    
    def uids_getter():
        #finding the companies links
        soup=bs(driver.page_source,"html.parser")
        UIDs=soup.find_all("a",{"href":"javascript:void(0)"})
        descs=soup.find_all("p",{"class":"descContent"})
        descs=descs[1:]
        DESC=[]
        for des in descs:
            DESC.append(des.text)
        UIDS=[]
        for UID in UIDs[2:]:
            UIDS.append(UID["data-pid"])
        return [UIDS,DESC]

    current_page=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,"//a[@class='is-current']")))
    data=[]
    pages=driver.find_elements(By.XPATH,"//li[@class='page-item no']")
    # current_page=driver.find_element(By.XPATH,"//a[@class='is-current']")
    # print(pages,'\n')
    while (pages[-1].text>current_page.text):
        data.extend(uids_getter())
        time.sleep(2)
        for pager in pages:
            if pager.text>=current_page.text:
                print('-------',pager.text,"---------\n")
                driver.execute_script("arguments[0].click();", pager)
                break
        # time.sleep(3)
        pages=driver.find_elements(By.XPATH,"//li[@class='no']")
        current_page=driver.find_element(By.XPATH,"//a[@class='is-current']")
        # print('\n\n',pages,"hjajajaja",pages[-1].text,' ',current_page.text)

    return data


from urllib.request import urlopen
import requests

def data_getter(deta):

    # url=url+"?p={}".format(n)  
    # session = requests.Session()
    # response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text

    # options = uc.ChromeOptions()
    # options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument("--window-size=1920,1080")
    # uc.TARGET_VERSION = 85
    # driver = uc.Chrome(options=options)
    # driver.maximize_window()
    time.sleep(1)



    # service = Service(ChromeDriverManager().install())
    # options = webdriver.ChromeOptions()
    # options.add_argument("--start-maximized")
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_argument("--disable-extensions")
    # options.add_argument("--disable-popup-blocking")
    # driver = webdriver.Chrome(service=service,options=options)

    import requests
    from urllib3.exceptions import InsecureRequestWarning
    from urllib3 import disable_warnings
    from urllib.request import urlopen
    import certifi
    print('\n',certifi.where(),'\n')
    data=[]
    print("started")
    disable_warnings(InsecureRequestWarning)
    for uid in deta[0]:
        url="https://partners.datadoghq.com/s/PartnerDirectoryDetails?pid="+uid 
        print(url)
        # u=urlopen(url)
        # page=u.read()


        # page = requests.get(url, verify=False)
        # print(page.content)

        # print(page.content)

        cookies = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}

        session = requests.Session()
        response = session.get(url, headers={'User-Agent': 'Mozilla/5.0','Cookie':'CONSENT=YES+cb.20210418-17-p0.it+FX+917; '},verify=False).text
        # print(response)

        # print("https://partners.datadoghq.com/s/PartnerDirectoryDetails?pid="+uid)
        # driver.get("https://partners.datadoghq.com/s/PartnerDirectoryDetails?pid="+uid)
        # ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        # driver.implicitly_wait(10)
        # WebDriverWait(driver,10).until(EC.url_to_be("https://partners.datadoghq.com/s/PartnerDirectoryDetails?pid="+uid))
        # WebDriverWait(driver,10).until(EC.url_matches("https://partners.datadoghq.com/s/PartnerDirectoryDetails?pid="+uid))
        # WebDriverWait(driver,10).until(EC.url_changes("https://partners.datadoghq.com/s/PartnerDirectoryDetails?pid="+uid))
        # if driver.current_url != "https://partners.datadoghq.com/s/PartnerDirectoryDetails?pid="+uid:
        #     driver.get("https://partners.datadoghq.com/s/PartnerDirectoryDetails?pid="+uid)
        # WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,"//div[@class='headh1 slds-truncate']")))
        # WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,"//div[@class='slds-form-element__control']")))
        soup=bs(response,"html.parser")
        print(soup.prettify())
        CN=soup.find("div",{"class":"headh1 slds-truncate"}).text
        info=soup.find_all("div",{"class":"slds-form-element__control"})
        datapoint=[CN,info[1],'Datadog',info[6],'missing',info[2],'prod/offering',deta[1][deta[0].index(uid)],'ceo','missing',info[5]]
        print(datapoint)
        data.append(datapoint)


    return data

print(data_getter([["0010e00001PEeQRAA1","0013200001AKQsLAAX"],["bla bla","alb alb"]]))