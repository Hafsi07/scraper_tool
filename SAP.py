from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv
import time

def spa(*args):
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
                searchphrase+=arg+"+"
        searchphrase=searchphrase[:-1]
    else: searchphrase='';print("searchphrase empty")

    url="https://pf-prod-sapit-partner-prod.cfapps.eu10.hana.ondemand.com/partnerNavigator?q="+searchphrase+"&page=1"
    driver.get(url)

    resnum=int(WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,"//div[@class='ds-filter-sort__sort-bar__results-counter__counter']"))).text)
    pages_number=resnum//12 if resnum%12==0 else (resnum//12)+1
    print(resnum,"  ",pages_number)
    try:
        elems=WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='ds-card__tile ds-flexCol-xs ds-flexCol-sm-6 ds-flexCol-lg-4 ds-p-none']")))
    except:
        return []
    print("SAP:")
    data=[]
    for i in  range(pages_number):
        url="https://pf-prod-sapit-partner-prod.cfapps.eu10.hana.ondemand.com/partnerNavigator?q="+searchphrase+"&page="+str(i+1)
        for j in range(len(elems)):
            driver.get(url)
            try:
                elems=WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='ds-card__tile ds-flexCol-xs ds-flexCol-sm-6 ds-flexCol-lg-4 ds-p-none']")))
                elems[j].click()
                time.sleep(1)
            except:
                continue
            #get data
            soup=bs(driver.page_source,"html.parser")
            try:
                srvs=soup.find_all("ul",{"class":"ds-list item-list ds-m-none service-item-size"})
                srvs=srvs[0].find_all("li")
                srvs=[i.text for i in  srvs]
            except:
                srvs=['missing']
            try:
                specs=soup.find_all("ul",{"class":"ds-list item-list ds-m-none service-item-size"})
                specs=specs[1].find_all("li")
                specs=[i.text for i in specs]
            except:
                specs=['missing']
            try:
                CN=soup.find("div",{"class":"partner-name--text"}).text
            except:
                CN='missing'
            try:
                try:
                    driver.find_element(By.XPATH,"//div[@class='ds-m-t-l service-prop-summary']").find_elements(By.TAG_NAME,"span")[1].click()
                except:
                    pass
                desc=' '.join(' '.join(soup.find("div",{"class":"ds-m-t-l service-prop-summary"}).text.split('\n')).split('\xa0'))
            except:
                desc='missing'
            try:
                places=soup.find_all("div",{"class":"address__line-1"})
                place=''
                for i in places:
                    place+=i.text
            except:
                place='missing'
            try:
                mail=soup.find("div",{"class":"address__email"}).text
            except:
                mail='missingg'
            try:
                link=soup.find_all("div",{"class":"partner-name--website"})[1].text
            except Exception:
                link=driver.find_element(By.XPATH,"//div[@class='partner-name--website']").text
            except:
                link='missing'
            datapoint=[CN,'missing','SAP',place,'missing','missing',specs,srvs,'missing',desc,'missing',mail,link]
            data.append(datapoint)
        print("scraped {0} elements".format(len(data)))
    return data


def dumperr(data,filename):
    with open(filename+'.csv','w',encoding='utf-8') as f: 
        wrote=csv.writer(f)
        wrote.writerow(['Company Name','Certification Rank','Vendor','HQ Location','Employee Count','Yr Founded', 'Specialisation','Services','Offerings','Short description','Ceo','Mail','URL'])
        wrote.writerows(data)
    print("terminated")

# dumperr(spa("Uruguay"),'hh')