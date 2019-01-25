#! /usr/bin/python3
import re
from urllib import parse
import requests
from bs4 import BeautifulSoup
import bs4
from lxml import etree
from selenium import webdriver
import time
import os

class Art:
    def __init__(self):
        self.id=0
        self.ArtType="E"
        self.name=""
        self.imdurl=""
        self.Authors=[]
        self.pubTime=""
        self.url=""

def WaitFor(driver,text,bPrint=True):
    while True:
        try:
            Text=driver.find_element_by_xpath("//*[@id='page']/div[1]/div[26]/div[2]/div/div/div/div[1]/div[1]/div/div/h3").text
            if Text.startswith(text):
                if not ("..." in Text):
                    break
        except:
            i=1
        time.sleep(1)
    if bPrint:
        print(driver.find_element_by_xpath("//*[@id='page']/div[1]/div[26]/div[2]/div/div/div/div[1]/div[1]/div/div/h3").text)

def GetArts(driver,Rid):
    ArticleType="0"
    try:
        title=driver.find_element_by_xpath("//*[@id='"+Rid+"']/div[3]/div[1]/div/a/value").text
        Turl=driver.find_element_by_xpath("//*[@id='"+Rid+"']/div[3]/div[1]/div/a").get_attribute('href')
        ArticleType="E"
    except:
        try:
            title=driver.find_element_by_xpath("//*[@id='"+Rid+"']/div[3]/div[1]/a/value").text
            Turl=driver.find_element_by_xpath("//*[@id='"+Rid+"']/div[3]/div[1]/a").get_attribute('href')
            ArticleType="C"
        except:
            title=""
            Turl=""
    return ArticleType,title,Turl

def geturl(driver,Name):
    driver.switch_to_window(driver.window_handles[0])
    #Str = "\""+Num+"\""
    #url = 'http://apps.webofknowledge.com/UA_GeneralSearch_input.do?product=UA&search_mode=GeneralSearch&SID=6CM2LNVOW3k7XSG549M&preferencesSaved='
    #url = 'http://apps.webofknowledge.com/UA_GeneralSearch_input.do?product=UA&search_mode=GeneralSearch&SID=5DO9FC4x8mgpPuLmFNP&preferencesSaved='
    url = 'http://apps.webofknowledge.com/'

    driver.get(url)
    Handle=driver.current_window_handle
    driver.find_element_by_id("clearIcon1").click() #点击清除输入框内原有缓存地址
    driver.find_element_by_id("value(input1)").send_keys(Name)#模拟在输入框输入入藏号
    driver.find_element_by_xpath("//*[@id='searchrow1']/td[2]/span/span[1]/span/span[2]/b").click()
    driver.find_element_by_xpath("//*[@id='select2-select1-results']/li[2]").click()
    #xxx=input("")
    driver.find_element_by_xpath("//*[@id='searchCell1']/span[1]").click()#模拟点击检索按钮

    WaitFor(driver,"Results")

    for id in range(1,11):
        Rid="RECORD_"+str(id)
        try:
            print(str(id-1)+"."+driver.find_element_by_xpath("//*[@id='"+Rid+"']/div[3]/div[1]/div/a/value").text)
        except:
            break
    sid=0
    #print(id)
    if id>2:
        sid=int(input("Which one? "))
    Rid="RECORD_"+str(sid+1)

    ArtList=[]
    tArt=Art()
    tArt.id=0
    tArt.ArtType,tArt.name,tArt.imdurl=GetArts(driver,Rid)
    if tArt.ArtType=="0":
        return ArtList
    ArtList.append(tArt)
    #outfile.write(str(0)+"|" + ArticleType+ "|"+title+ "|"+ Turl+"\n")
    try:
        driver.find_element_by_xpath("//*[@id='"+Rid+"']/div[4]/div[1]/a").click()
    except:
        return ArtList

    WaitFor(driver,"Citing")

    Tid=1
    while True:
        for id in range(1,11):
            Rid="RECORD_"+str(Tid)
            tArt=Art()
            tArt.id=Tid
            tArt.ArtType,tArt.name,tArt.imdurl=GetArts(driver,Rid)
            if tArt.ArtType=="0":
                return ArtList
            ArtList.append(tArt)
            #outfile.write(str(Tid)+"|" + ArticleType+ "|"+title+ "|"+ Turl+"\n")
            Tid=Tid+1
        #return ArtList
        try:
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='summary_navigation']/nav/table/tbody/tr/td[3]/a").click()
            WaitFor(driver,"Citing",False)
        except:
            return ArtList

def GetArtInfo(driver,Tart):
    driver.switch_to_window(driver.window_handles[0])
    #url = 'http://apps.webofknowledge.com/full_record.do?product=UA&search_mode=CitingArticles&qid=36&SID=6CM2LNVOW3k7XSG549M&page=1&doc=1'
    driver.get(Tart.imdurl)
    id=1
    Authors=[]
    ArticleType=Tart.ArtType
    divID=2
    while not driver.find_element_by_xpath("//*[@id='records_form']/div/div/div/div[1]/div/div["+str(divID)+"]").text.startswith("By"):
        divID=divID+1
    #if ArticleType=='E':
    #    divID=2
    #else:
    #    divID=3
    #if driver.find_element_by_xpath("//*[@id='records_form']/div/div/div/div[1]/div/div["+str(divID)+"]").text.startswith("Associated Data"):
    #    divID=divID+1
    while True:
        try:
            #if ArticleType=='E':
            #    #if driver.find_element_by_xpath("//*[@id='records_form']/div/div/div/div[1]/div/div[2]").
            #    Author=driver.find_element_by_xpath("//*[@id='records_form']/div/div/div/div[1]/div/div["+str(divID)+"]/p/a["+str(id)+"]").text
            #else:
            Author=driver.find_element_by_xpath("//*[@id='records_form']/div/div/div/div[1]/div/div["+str(divID)+"]/p[1]/a["+str(id)+"]").text
            id=id+1
            #print(Author)
            Authors.append(Author)
        except:
            break
    print(Authors)
    divID=divID+1
    
    subID=1
    try:
        while not driver.find_element_by_xpath("//*[@id='records_form']/div/div/div/div[1]/div/div["+str(divID)+"]/p["+str(subID)+"]").text.startswith("Published"):
            subID=subID+1
        pubTime=driver.find_element_by_xpath("//*[@id='records_form']/div/div/div/div[1]/div/div["+str(divID)+"]/p["+str(subID)+"]").text
    except:
        pubTime=""

    print(pubTime)
    #driver.find_element_by_xpath("//*[@id='buttonftIconSpan']").click()
    #time.sleep(1)
    #if 1:
    #print(driver.find_element_by_xpath("/html/body/div[1]/div[26]/div/div/div/div[2]/div/div/span/ul/li[1]").text)
    try:
        if driver.find_element_by_xpath("//*[@id='solo_full_text_1']").startswith("Full Text from Publisher"):
            driver.find_element_by_xpath("//*[@id='solo_full_text_1']").click()
        else:
            raise NameError("Need Select")
    except:
        try:
            driver.find_element_by_xpath("//*[@id='buttonftIconSpan']").click()
            time.sleep(1)
            if driver.find_element_by_xpath("/html/body/div[1]/div[26]/div/div/div/div[2]/div/div/span/ul/li[1]/a").text.startswith("Full Text from Publisher"):
                driver.find_element_by_xpath("/html/body/div[1]/div[26]/div/div/div/div[2]/div/div/span/ul/li[1]/a").click()
            else:
                raise NameError("No Full Text")
        except:
            url="No_Full_Text"

        time.sleep(1)
    try:
        driver.switch_to_window(driver.window_handles[1])
        bLoop=True
        while bLoop:
            time.sleep(1)
            #print (driver.current_url)
            if driver.current_url != "about:blank":
                bLoop=False
        time.sleep(1)
        url=driver.current_url
        time.sleep(1)
        driver.close()
    except:
        url="No_Full_Text"
    return Authors,pubTime,url

def PrtArt(outfile,Art,State):
    outfile.write(str(Art.id)+"|"+Art.ArtType+"|"+Art.name+"|"+str(Art.Authors)+"|"+Art.pubTime+"|"+State+"|"+Art.url+"\r\n")

def RefAnalysis(driver,ArtList,outfile):
    for Art in ArtList:
        try:
            Art.Authors,Art.pubTime,Art.url=GetArtInfo(driver,Art)
        except:
            try:
                Art.Authors,Art.pubTime,Art.url=GetArtInfo(driver,Art)
            except:
                try:
                    Art.Authors,Art.pubTime,Art.url=GetArtInfo(driver,Art)
                except:
                    raise NameError("failed 3 times")
    
    AuthorSet=set(ArtList[0].Authors)
    PrtArt(outfile,ArtList[0],"Ori")
    for i in range(1,len(ArtList)):
        State="Other"
        for Author in ArtList[i].Authors:
            if Author in AuthorSet:
                State="Self"
        PrtArt(outfile,ArtList[i],State)




def main():
    uinfo=[]
    driver = webdriver.Firefox()
    #inpfile=open("list.txt","r")
    #ArtList=inpfile.readlines()
    #inpfile.close()
    #for line in ArtList:
    #    if line[0]=='#':
    #        continue
    while True:
        line=input("Enter cmd:\n")
        if line.startswith("#exit"):
            break
        info=line.strip("\n").split('|')
        #print(line)
        #print(info)
        Aid=info[0]
        Name =info[1]
        outfile=open("data/"+Aid+".txt","w")
        ArtList=geturl(driver,Name)
        print(len(ArtList))
        RefAnalysis(driver,ArtList,outfile)
        outfile.close()
        #os.system("cat data/"+Aid+".txt |wc -l")
    
    driver.close()

main()
