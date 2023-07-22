from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

    
def datawer(*args):
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
    else: searchphrase='.';print("searchphrase empty")

    url="https://partner-finder.oracle.com/catalog/"
    driver.get(url)

    # preparing the filters in first phase
    g=WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,'//div[@class="o-partner-search--dropdown"]'))) #click the search options
    g.click()
    a=WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.ID,'search-dropdownitem'))) #select all option
    a.click()
    time.sleep(1)
    search_field=driver.find_element(By.XPATH,'//input[@id="search-fld"]')
    search_field.send_keys(searchphrase)
    search_field.send_keys(Keys.RETURN)

    # determining the pages number
    time.sleep(4)
    print("Oracle:")
    while (True):
        try:
            resnum=int(WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,'//span[@class="o-value"]'))).text)
            break
        except:
            time.sleep(1)
    print(resnum)
    pages_number=resnum//15 if resnum%15==0 else (resnum//15)+1

    links=[]
    for i in range(pages_number):
        try:
            urls=WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="o-partner--info"]')))
            urlse=[x.find_element(By.TAG_NAME,"a").get_attribute('href') for x in urls]
            links=links+urlse
        except Exception:
            urls=WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="o-partner--info"]')))
            urlse=[x.find_element(By.TAG_NAME,"a").get_attribute('href') for x in urls]
            links+=urlse
        except:
            pages_number+=1
            continue
        time.sleep(3)
        next=WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,'//li[@class="pagination-buttons"]')))
        next[-1].click()
        time.sleep(5)
        break
        
    print("Got elements links")
    data=[]
    for link in links:
        driver.refresh()
        driver.get(link)

        try: 
            urle=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,'//div[@id="companyURL"]//*')))
            urle=urle.text
        except Exception :
            print(Exception)
            urle='missing'
            print('misss')
        try:
            adr=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,'//div[@class="o-partner-businesscard--address"]')))
            adr=' '.join(adr.text).split('\n')
        except:
            adr='missing'
        try:
            CN=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
            CN=CN.text
        except:
            CN='missing'
        try:
            desc=' '.join(WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID,"PartnerSummary"))).text.split('\n'))
        except:
            desc='missing'
        driver.get(link+"#profile-expertise")
        try:
            serv=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID,"list_ImpOrManage")))
            servi=serv.find_elements(By.TAG_NAME,"li")
            specs=[x.text for x in servi]
        except:
            specs=['missing']

        try:
            off=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID,"list_LicAndHW")))
            offer=off.find_elements(By.TAG_NAME,"li")
            offerings=[x.text for x in offer]
        except:
            offerings=['missing']

        try:
            servic=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID,"expertise_list_LicAndHW_765")))
            service=servic.find_elements(By.TAG_NAME,"li")
            services=[x.text for x in service]
        except:
            services=['missing']
        
        datapoint=[CN,'missing','hubspot',adr,'missing','missing',specs,services,offerings,desc,'missing',urle]
        data.append(datapoint)
    print("scraped {0} elements".format(len(data)))
    return data