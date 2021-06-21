from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests
starturl="https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
browser=webdriver.Chrome("./chromedriver")
Data=[]
NewPlanetData=[]
browser.get(starturl)
time.sleep(10)
def Scrape():
   

    for i in range(0,428):
        while True:
            time.sleep(2)
            soup=BeautifulSoup(browser.page_source,"html.parser")
            currentPageNo=int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
            if currentPageNo<i:
                 browser.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]').click()
            elif currentPageNo>i:
                 browser.find_element_by_xpath('//*//*[@id="mw-content-text"]/div[1]').click()
            else:
                break
        for ultag in soup.find_all("ul",attrs={"class","exoplanet"}):
            litags=ultag.find_all("li")
            templist=[]
            for index,litag in enumerate(litags):
                if index==0:
                    templist.append(litag.find_all("a")[0].contents[0])
                else:
                    try:
                        templist.append(litag.contents[0])
                    except:
                        templist.append("")
            hyperlinklitag=litags[0]
            templist.append("https://https://en.wikipedia.org/wiki/List_of_brown_dwarfs"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            Data.append(templist)
        browser.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]').click()
        print(f"{i}pagedone1")

def ScrapeMoreData(hyperlink):
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.parser")
        templist=[]
        for trtag in soup.find_all("tr",attrs={"class":"fact_row"}):
            tdtags=trtag.find_all("td")
            for tdtag in tdtags:
                try:
                    templist.append(tdtag.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    templist.append("")
        NewData.append(templist)
    except:
        time.sleep(1)
        ScrapeMoreData(hyperlink)

Scrape()
for index,data in enumerate(Data):
    ScrapeMoreData(data[5])
    print(f"{index+1}pagedone2")
FinalData=[]  
for index,data in enumerate(Data):
    NewDataElement=NewData[index]      
    NewDataElement=[elem.replace("\n","")for elem in NewDataElement]
    NewDataElement=NewData[:7]
    FinalData.append(data+NewDataElement)
with open("scrapper_2.csv","w")as f:
    csvwriter=csv.writer(f)
    csvwriter.writerrow(Headers)
    csvwriter.writerrows(FinalData)
