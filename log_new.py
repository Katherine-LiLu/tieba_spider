#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib
from lxml import etree
import requests
import re
from bs4 import BeautifulSoup
import time


def read_HTML(url):
    file = urllib.request.urlopen(url)
    data = file.read()
    return data


def scrapy(url):
    name = []
    author = []
    list1 = []
    global cnb
    data = read_HTML(url)
    html = etree.HTML(data)
    ##帖子名字
    ft = html.xpath("//a[@class='j_th_tit ']")
    for i in ft:
        name.append(i.text)
        # print(i.text)
    # print(len(name))
    ##帖子链接
    link = html.xpath("//a[@class='j_th_tit ']/@href")
    #for i in link:
    #    ss = i

    ##作者以及最近的回复者
    # sd = html.xpath("//a[@class='frs-author-name j_user_card ']")
    # for i in sd:
    #     print(i.text)
    #主题作者
    st = html.xpath("//span[@class='tb_icon_author ']")
    for i in st:
        a = i.attrib.get('title')
        # print(a)
        author.append(a)
    # print(len(author))
    # for i in range(len(name)):
    #     ws.write(i+1,0,name[i])
    #     ws.write(i+1,1,author[i])
    #   cnb += 1

    ps = html.xpath('//span[@class="red_text"]')
    for i in ps:
        list1.append(int(int(i.text)/50+1))
    pags = list1[0]
    return link,pags


def findname(soup):
    nname = ''
    cname = ''
    mname = ''
    tname = ''
    #name = soup.find_all('h3', class_="core_title_txt pull-left text-overflow ")
    name = soup.find_all('h3')[0]
    #if name == None:
    #    name = soup.find('h3', class_="core_title_txt pull-left text-overflow   vip_red ")
    if name != None:
        pname = name.get_text()
        if re.search('\?', pname) != None:
            pname = pname.split('?')[0]
        if re.search('\:', pname) != None:
            for i in pname.split(':'):
                mname = mname + i
            pname = mname
        if re.search('\*', pname) != None:
            pname = pname.split('*')[0]
        if re.search('\|', pname) != None:
            pname = pname.split('|')[0]
        if re.search('\<', pname) != None:
            pname = pname.split('<')[0]
        if re.search('\>', pname) != None:
            pname = pname.split('>')[0]
        if re.search('\"', pname) != None:
            pname = pname.split('"')[0]
        if re.search('\r', pname) != None:
            pname = pname.split('\r')[0]
        if re.search('\n', pname) != None:
            pname = pname.split('\n')[0]
        if re.search('\/', pname) != None:
            for i in pname.split('/'):
                tname = tname + i
            pname = tname
        if re.search('\.', pname) != None:
            for i in pname.split('.'):
                nname = nname + i
            pname = nname
        for i in pname.split(' '):
            cname = cname + i
        pname = cname
        pname = pname.split('\\')[0]
    else:
        pname = None

    return pname


def test1(url):
    results_list=[]

    maxtrytime = 5
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
               'Connection': 'close'}
    data1=None
    for trys in range(maxtrytime):
        try:
            data1 = requests.get(url, headers=headers)
            break
        except:
            if trys < maxtrytime-1:
                continue
            else:
                break
    time.sleep(0.3)
    content = data1.text
    soup = BeautifulSoup(content, 'html.parser')

    if soup.title.string != "贴吧404":
        limit = soup.find_all('span', class_='red')
        page = limit[1].get_text()
        for k in range(int(page)):
            url1 = url+"?pn="+str(k+1)
            print(url1)
            maxtrytime = 5
            for trys in range(maxtrytime):
                try:
                    data1 = requests.get(url1, headers=headers)
                    break
                except:
                    if trys < maxtrytime-1:
                        continue
                    else:
                        break
            time.sleep(0.3)
            content = data1.text
            soup = BeautifulSoup(content, 'html.parser')

            
            for i in soup.find_all('div',class_='l_post l_post_bright j_l_post clearfix'):
                #对于每一个回帖
                # ##找到回复
                # print(str(i))
                username=' '
                floornum=' '
                posttime=' '
                postcontent=' '
                
                rep = i.find('div', class_='d_post_content j_d_post_content')
                if rep != None:
                    postcontent=rep.get_text()
                    # print(rep.get_text())
                    #ws.write(0, 3*rnb, rep.get_text())
                ##找时间
                # te = re.findall(r'"date":"(.+?)"',str(i))
                # floor = re.findall(r'"post_no":(.+?),"',str(i))
                # ws.write(cnb, 3 * rnb + 1, te.pop() +" "+floor.pop()+"楼")
                ##找时间
                te = i.find_all('span', class_="tail-info")
                # for i in te:
                #     print(i.get_text())
                if te !=None:
                    floornum=te[-2].get_text()[:-1]
                    posttime=te[-1].get_text()
                

                ##找人
                pp = i.find('a', class_='p_author_name')
                if pp != None:
                    username=pp.get_text()
                results_list.append(username)
                results_list.append(floornum)
                results_list.append(posttime)
                results_list.append(postcontent)
    return results_list
                        



if __name__ == "__main__":
    filename = 'data.csv'
    for j in range(0, 2):
        x = urllib.request.quote("柯南")
        href,pgs = scrapy("https://tieba.baidu.com/f?kw="+x+"&pn="+str(j*50))
        for i in href:
            path = "https://tieba.baidu.com"+i
            #path='https://tieba.baidu.com/p/6521477887'
            try:
                results=test1(path)
                with open(filename, 'a') as file_object:
                    for content in results:
                        if content!=results[-1]:
                            file_object.write(content)
                            file_object.write(',')
                        else:
                            file_object.write(content)
                            file_object.write('\n')
            except:
                print('except')
            
