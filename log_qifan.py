# -*- coding: utf-8 -*-
import urllib
import os
from lxml import etree
import requests
import re
from bs4 import BeautifulSoup
import time
from Until import getTimeAndFloor
import csv

session = requests.session()

requests.adapters.DEFAULT_RETRIES = 5

##行序号
cnb = 0
num = 0

textpath = 'text/'

def read_HTML(url):
    file = urllib.request.urlopen(url)
    data = file.read()
    return data


def scrapy(url):
    list1 = []
    #global cnb
    data = read_HTML(url)
    html = etree.HTML(data)
   
    ##帖子链接
    link = html.xpath("//a[@class='j_th_tit ']/@href")
   
    ps = html.xpath('//span[@class="red_text"]')
    for i in ps:
        list1.append(int(int(i.text)/50+1))
    pags = list1[0]
    return link,pags

def CrawlPost(url):
    global num
    global cnb
    ##列序号
    rnb = 0
    rp = []
    rpt = []
    rpu = []
    maxtrytime = 10
    headers = {
            #'Cookie':'TIEBAUID=a62b21a2c643881449f4bb54; TIEBA_USERTYPE=df77991dd15aac86d8a2f857; BAIDUID=5B4950A99E5727E59B4EAA181CBBB666:FG=1; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1556628646; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1556631206; BDUSS=3gtSnJVZHhydHBQaUE2WTFvTVY2OEV0TXZTczVKblBVSngzM0lCTnR6VGIwZTljRVFBQUFBJCQAAAAAAAAAAAEAAABRQtNfzOzN9bjHtdi7orChxOMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANtEyFzbRMhcc; STOKEN=68c97ecf87d6e400fa4c8fcb786cb3c9b080cc49f3c19a7c4cdaf49c41e3e070; wise_device=0; 1607680593_FRSVideoUploadTip=1; BIDUPSID=3F2962181D0227C2BC4AA03B390B1C06; PSTM=1556631240; BDRCVFR[gltLrB7qNCt]=mk3SLVN4HKm; delPer=0; PSINO=3; H_PS_PSSID=1469_21098_28775_28722_28964_28834_28585_28603; BDORZ=FFFB88E999055A3F8A630C64834BD6D0',
            #'Host':'tieba.baidu.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Connection': 'close'
    }
    for trys in range(maxtrytime):
        try:
            data1 = requests.get(url, headers=headers)
            break
        except:
            if trys < maxtrytime-1:
                continue
            else:
                break
    content = data1.text
    soup = BeautifulSoup(content, 'html.parser')
    content = []  # 发帖内容
    info = []  # infomation
    userid = []

    ##找到每一个帖子下面的回复
    dt = soup.find_all('div', class_="d_post_content j_d_post_content")
    for i in dt:
        content.append(i.get_text())
       # print(i.get_text())
        # ##找到回复的时间
    tm = soup.find_all('div', class_="post-tail-wrap")
    for i in tm:
        info.append(i.get_text())
     
    # ##找到发回复的人
    rpp = soup.find_all('a', class_='p_author_name')
    for i in rpp:
       # print(i.get_text())
        userid.append(i.get_text())
    result = []
    for i in range(len(content)):
        result.append(userid[i])
        timeinfo, floorinfo = getTimeAndFloor(info[i])
        result.append(floorinfo)
        result.append(timeinfo)
        result.append(content[i])
        
    return result
    # rpu[i] 名字  月夜轻衫5565
    # rpt[i] 发帖信息 来自Android客户端21楼2020-01-26 07:17
    # rp[i]  平和版计时引爆摩天楼。 内容
    

def getPageCount(url):
    limit = 50000000
    data = read_HTML(url)
    html = etree.HTML(data)
    ps = html.xpath('//span[@class="red"]')
    try:
        count = int(ps[1].text)
        return min(count, limit)
    except:
        return 1




if __name__ == "__main__":

    x = urllib.request.quote("柯南")

    fpath = 'data.csv'
    # 柯南吧url https://tieba.baidu.com/f?kw=柯南
    href, pags = scrapy("https://tieba.baidu.com/f?kw=" + x)
    for pn in range(0, 200):
        try:
            # 一页有50个帖子
            # href, pgs = scrapy("https://tieba.baidu.com/f?kw=" + x + "&pn=" + str(pn * 50))
            for h in href:
                path = "https://tieba.baidu.com" + h
                print(path)
                # 一个帖子下面的页数
                pageCount = getPageCount(path)
                result = []
        
            
                for i in range(pageCount):
                    tmp = path + '?pn=' + str(i+1)
                    result = result + CrawlPost(tmp)
            
            
                with open(fpath,'a+', encoding='utf-8', newline='') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(result)
                    print("写入一条 长度为", len(result))
        except:
            print("expect")

