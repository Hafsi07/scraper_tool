from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time 
from linkedin import cleaner
t1=time.time()

def atlassian_scraper(CN="",loc="",cntr="",spec="",prod="",serv=""):
    '''scrape the atlassian website depending on the filters provided'''
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service,options=options)

    driver.get("https://partnerdirectory.atlassian.com/")

    #company name
    try:
        if CN=='company_name': 
            CN=''
        company_name=driver.find_element(By.XPATH,'//input[@id="thePage:theForm:userText"]')
        company_name.click()
        company_name.send_keys(CN)
    except:
        pass
    #location address
    try:
        if loc=='Location':
            loc=''
        location=driver.find_element(By.XPATH,'//input[@id="thePage:theForm:userLoc"]')
        location.send_keys(loc)
    except:
        pass
    #country
    try:
        if cntr=="Country":
            cntr=''
        country=driver.find_element(By.XPATH,'//select[@id="thePage:theForm:userCountry"]')
        country.send_keys(cntr)
    except:
        pass

    soup=bs(driver.page_source,"html.parser")

    #finding specializations 
    specs=soup.find("select",{"id":"thePage:theForm:rptSearchStd:0:MULTISELECT"}).find_all("option")
    specs=[i.text for i in specs]
    # print("Specialisations :\n",specs,"\n")

    #finding products
    prods=soup.find("select",{"id":"thePage:theForm:rptSearchStd:1:MULTISELECT"}).find_all("option")
    prods=[i.text for i in prods]
    # print("Products :\n",prods,"\n")


    #finding services
    services=soup.find("select",{"id":"thePage:theForm:rptSearchStd:2:MULTISELECT"}).find_all("option")
    services=[i.text for i in services]
    # print("Services :\n",services,"\n")



    #specialization
    try:
        if spec=="specializations":
            spec=''
        specia=driver.find_element(By.XPATH,'//select[@id="thePage:theForm:rptSearchStd:0:MULTISELECT"]')
        specia.send_keys(spec)
    except: pass
    #product
    try:
        if prod=="products":
            prod=''
        product=driver.find_element(By.XPATH,"//select[@id='thePage:theForm:rptSearchStd:1:MULTISELECT']")
        product.send_keys(prod)
    except:
        pass
    

    #product
    try:
        if serv=="services":
            serv=''
        servs=driver.find_element(By.XPATH,'//select[@id="thePage:theForm:rptSearchStd:1:MULTISELECT"]')
        servs.send_keys(serv)
    except:
        pass 
    time.sleep(3)
    location.send_keys(Keys.RETURN)
    time.sleep(2)
    print("Atlassian:")
    def hedhi():
        '''scrapes the page where the driver is at currently retreiving all the companies in that page'''
        try:
            #see if there are no results to the search 
            warning=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID,"thePage:theForm:optResultsNone")))
            if (warning!=None):
                print("no results")
                return([])
        except:
            time.sleep(2)
            driver.implicitly_wait(2)
            elements=driver.find_elements(By.XPATH,"//a[@class='pl-results-partner-name']")
            time.sleep(5)
            elements=driver.find_elements(By.XPATH,"//a[@class='pl-results-partner-name']")
            data=[]
            time.sleep(3)
            #going through the elements of the page one by one
            for element in elements:
                datapoint=[]
                try:
                    element.click()
                except:
                    continue
                time.sleep(5)
                soup=bs(driver.page_source,"html.parser")
                try:
                    ratings=soup.find("span",{"id":"thePage:theForm:partnerType"}).ul.li.text
                except: 
                    ratings="missing"
                try:
                    CN=soup.find("h2",{"class":"pl-partner-name"}).text
                except: CN="missing"
                try:descs=' '.join(soup.find("p",{"id":"povDetails"}).find("span",{"class":"hidden-xs"}).span.text.split('\n'))
                except:descs="missing"
                try:
                    products=soup.find("span",{"id":"thePage:theForm:rptPDetails:0:PartnerDetail"}).div.find_all("div")
                    products=[i.text for i in  products]
                except: products=['missing']
                try:
                    srvs=soup.find("span",{"id":"thePage:theForm:rptPDetails:1:PartnerDetail"}).div.find_all("div")
                    srvs=[i.text for i in  srvs]
                except: srvs=["missing"]
                try:
                    place=soup.find("ul",{"class":"list-group pl-location-details"}).li.span.text
                except:
                    place="missing"
                # phone=soup.find("li",{"class":"list-group-item pl-location-phone pl-location-plocez__Phone__c"}).span.a.text
                try:
                    mail=soup.find("li",{"class":"list-group-item pl-location-email pl-location-plocez__Email__c"}).span.a.text
                except:
                    mail="none found"
                try:
                    url=soup.find("span",{"id":"thePage:theForm:rptLocContact:3:urlValue"}).text
                except: url="missing"
                try: 
                    employerscount=soup.find("span",{"id":"thePage:theForm:rptLOV:2:LocationOverview"}).text
                except: employerscount="missing"
                datapoint=[CN,ratings,'Atlassian',place,employerscount,'missing',products,srvs,'missing',descs,'missing',mail,url]
                data.append(datapoint)
                time.sleep(1)
                ActionChains(driver).send_keys(Keys.ESCAPE).perform() #escape key to close the popup page
                time.sleep(1)  
            return(data)

    donnee=[]
    #going through all the pages on the website and scraping the companies profiles 
    print("scraping elements now...")
    while (True):
        sk=hedhi()
        if sk==[]: return []
        #breaking condition: no more new data to scrape
        if(len(donnee)!=0 and donnee[(len(donnee)//12)*12:]==sk):
            break
        donnee+=sk
        print("scraped ",len(sk)," elements for a total of ",len(donnee))
        try:
            btn=driver.find_element(By.XPATH,"//span[@title='Next Page']")
            btn.click()
        except: 
            pass
    driver.quit()
    return donnee 

def dumperr(data,filename):
    if filename=="":
        filename="Default_name"
    if data==[]: 
        print("no data")
        return "No data found"
    datta=cleaner(data)
    with open(filename+'.csv','w',encoding='utf-8') as f: 
        wrote=csv.writer(f)
        wrote.writerow(['Company Name','Certification Rank','Vendor','HQ Location','Employee Count','Yr Founded', 'Specialisation','Services','Offerings','Short description','Ceo','Mail','URL'])
        wrote.writerows(datta)
    print("terminated")

