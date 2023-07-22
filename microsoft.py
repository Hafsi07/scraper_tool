from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from selenium.webdriver.common.action_chains import ActionChains


def micro(*args):
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

    url = ';radius=100;freetext='+searchphrase+';suggestion=true;locationNotRequired=true'

    data=[]
    f=18
    n=0
    print("Microsoft:")
    while n<f:
        mURL= 'https://main.prod.marketplacepartnerdirectory.azure.com/en-US/partners?filter=sort=0;pageSize=18;pageOffset='+str(n)+url
        if n==0:
            mURL='https://main.prod.marketplacepartnerdirectory.azure.com/en-US/partners?filter=sort=0;pageSize=18;'+url
        driver.get(mURL)
        try: 
            elems=WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.XPATH,"//span[@class='ms-Button-textContainer textContainer-90']")))
            print("no results\n")
            return []
        except:
            pass
        try:
            elems=WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='tile-container card ms-depth-8']")))
        except: 
            continue
        try:
            WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,'//span[contains(text(),"Next")]')))
            f+=18
        except:
            pass
        
        for j in range(len(elems)):
            if n==0:
                mURL='https://main.prod.marketplacepartnerdirectory.azure.com/en-US/partners?filter=sort=0;pageSize=18;'+url
            driver.get(mURL)

            try:
                elems=WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='tile-container card ms-depth-8']")))
                elems[j].click()
                time.sleep(1)
            except:
                continue
            #get data
            try:
                desc=' '.join(driver.find_element(By.XPATH,"//div[@class='partner-description']").text.split('\n'))
            except:
                desc='missing'
            
            try:
                srvv=driver.find_elements(By.XPATH,"//ul[@class='description-ul']")[3].find_elements(By.TAG_NAME,"li")
                if len(srvv==4):
                    srvv=driver.find_elements(By.XPATH,"//ul[@class='description-ul']")[0].find_elements(By.TAG_NAME,"li")

                srvs=[i.text for i in  srvv]
            except:
                srvs=['missing']
            
            try:
                srvv=driver.find_elements(By.XPATH,"//ul[@class='description-ul']")[4].find_elements(By.TAG_NAME,"li")
                if len(srvv==4):
                    srvv=driver.find_elements(By.XPATH,"//ul[@class='description-ul']")[0].find_elements(By.TAG_NAME,"li")
                offerings=[i.text for i in  srvv]
            except:
                offerings=['missing']

            try:
                srvv=driver.find_elements(By.XPATH,"//ul[@class='description-ul']")[-1].find_elements(By.TAG_NAME,"li")
                if len(srvv==4):
                    srvv=driver.find_elements(By.XPATH,"//ul[@class='description-ul']")[0].find_elements(By.TAG_NAME,"li")
                products=[i.text for i in  srvv]
            except:
                products=['missing']
            
            try:
                CN=driver.find_element(By.TAG_NAME,"h1").text
            except:
                CN='missing'
            

            try:
                driver.find_element(By.XPATH,"//a[@title='Additional information']").click()
                link=driver.find_element(By.XPATH,"//a[@class='ms-Link c-hyperlink website-link root-147']").get_attribute('href')
            except:
                try:
                    driver.find_element(By.XPATH,"//a[@title='Additional information']").click()
                    link=driver.find_element(By.XPATH,"//a[@class='ms-Link c-hyperlink website-link root-136']").get_attribute('href')
                except:
                    link='linkmissing'
            try:
                driver.find_element(By.XPATH,"//a[@title='Additional information']").click()
                place=driver.find_elements(By.XPATH,"//span[@class='ms-Button-flexContainer flexContainer-56']")[-1].text
            except:
                place='missing'
                
            datapoint=[CN,'missing','Microsoft',place,'missing','missing',products,srvs,offerings,desc,'missing','missing',link]
            data.append(datapoint)
        print("scraped {0} elements".format(len(data)))
        
        n+=18
    return data


def dumperr(data,filename):
    with open(filename+'.csv','w',encoding='utf-8') as f: 
        wrote=csv.writer(f)
        wrote.writerow(['Company Name','Certification Rank','Vendor','HQ Location','Employee Count','Yr Founded', 'Specialisation','Services','Offerings','Short description','Ceo','Mail','URL'])
        wrote.writerows(data)
    print("terminated")

# dumperr(micro(),"microooo")
