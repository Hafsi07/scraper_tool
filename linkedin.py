from selenium import webdriver
import csv
from bs4 import BeautifulSoup as bs 
from urllib.request import urlopen,Request
import requests


def cleaner(data):
    # print("Data length before cleaning: ",len(data))
    # fresh_data=list(set(data))
    # print("Data length after cleaning: ",len(fresh_data))
    

    driver=webdriver.Chrome()
    driver.get("https://www.linkedin.com")
    coockies={}
    for coockie in driver.get_cookies():
        coockies[coockie['name']]=coockie['value']

    driver.close()
    fresh_data=data
    newdata=[]
    for datapoint in fresh_data:
        new_datapoint=datapoint
        if datapoint[0]!='missing':
            url =( "https://www.linkedin.com/search/results/all/?keywords="+datapoint[0]+"&origin=GLOBAL_SEARCH_HEADER&sid=SCi").replace(' ','%20')
            print(url)
        else : break
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

        response = requests.get(url, headers=headers,cookies=coockies)
        

        soup=bs(response.content,"html.parser")
        print(soup)
        url=soup.find("a",{"class":"app-aware-link  scale-down "})['href']

        response=requests.get(url,headers=headers,cookies=coockies)
        
        soup=bs(response.content,"html.parser")
        print(soup)
        try:
            members=int(soup.find("a",{"class":"mt1 t-14 t-black--light"}).text.split(' ')[0])
            description=soup.find("div",{"class":"groups-guest-view__truncate mt4"}).find("span",{"dir":"ltr"}).text
            ceo=soup.find("div",{"class":"ui-entity-action-row mv3"}).find("div",{"class":"artdeco-entity-lockup__title ember-view"}).text
            year_founded=soup.find_all("p",{"class":"t-14 t-black--light"})[-1].text
        except:
            try: 
                description=soup.find_all("p")[1].text
            except:
                description='missing'
            try:
                all=soup.find_all("dd")
                members=all[2].text.split(' ')[0]
                year_founded=all[-1].text
            except:
                members=year_founded='missing'
            ceo='missing'

        if year_founded!=members : 
            new_datapoint[5]=year_founded if(datapoint[5]=='missing')else datapoint[5]
        
        if datapoint[9]=='missing':
            new_datapoint[9]=description
        if datapoint[10]=='missing':
            new_datapoint[10]=ceo
        if datapoint[4]=='missing':
            new_datapoint[4]=members
        newdata.append(new_datapoint)
    return newdata
with open('awsdeleted.csv','r',encoding='utf-8') as f:
    data=csv.reader(f)
    n=0
    datta=[]
    for row in data:
        if n==0:
            n+=1
            continue
        n+=1
        if n%2!=1:
            continue
        datta.append(row)
        # n+=1
print(cleaner(datta))

        