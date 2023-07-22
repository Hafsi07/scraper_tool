import csv
import requests
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.8',
    'Referer': 'https://www.example.com/',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json'
}
def summer(*args):
    searchphrase=''
    if args:
        for arg in args:
            if arg!='':
                searchphrase+=arg+"+"
        searchphrase=searchphrase[:-1]
    else: searchphrase='';print("searchphrase empty")


    url = 'https://channel.smartsheet.com/directory/search?q='+searchphrase
    return urls_get(url)


def urls_get(mURL):
    response = requests.get(mURL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        resnum=int(soup.find("div",{"class":"col-xs-6"}).find_all("p")[-1].b.text)
        pages_number=resnum//10 if resnum%10==0 else (resnum//10)+1
    except:
        return []
    try:
        pass
    except Exception:
        print(Exception)
        pages_number=10
    print("SmartSheet:")
    urls=[]
    for i in range(pages_number):
        url = 'https://channel.smartsheet.com/directory/search?q=d'+'&p='+str(i)

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        elems=soup.find_all("a",{"class":"btn btn-default"})
        elems=[i['href'] for i in elems]
        urls+=elems
    print("Got the elements URLs")
    data=[]
    for url in urls:
        try:
            url="https://channel.smartsheet.com"+url
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
        except:
            continue
        try:
            CN=soup.find("h4").text
        except Exception:
            CN=soup.find("img",{"id":"Locator_BodyContent_PartnerLogo"})['alt']
        except:
            CN='missing'

        try:
            link=soup.find("a",{"target":"_blank"}).text
        except:
            link='missing'
        try:
            place=' '.join(' '.join(soup.find("address",{"itemprop":"address"}).text.split('\n')).split('\xa0'))
        except:
            place='missing'
        try:
            desc=' '.join(' '.join(soup.find("p",{"id":"Locator_BodyContent_MarketplaceLongDescription"}).text.split('\n')).split('\xa0'))
        except:
            desc='missing'
        try:
            srvs=soup.find_all("h3",{"class":"text-center locator__sub-header"})
            srvs=[i.text for i in srvs]
        except:
            srvs=['missing']
        datapoint=[CN,'missing','SmartSheet',place,'missing','missing','missing',srvs,'missing',desc,'missing','missing',link]
        data.append(datapoint)
    print("scraped {0} elements".format(len(data)))
    return data

def dumperr(data,filename):
    with open(filename+'.csv','w',encoding='utf-8') as f: 
        wrote=csv.writer(f)
        wrote.writerow(['Company Name','Certification Rank','Vendor','HQ Location','Employee Count','Yr Founded', 'Specialisation','Services','Offerings','Short description','Ceo','Mail','URL'])
        wrote.writerows(data)
    print("terminated")
# dumperr(summer('uruguay'),'stylesheet')