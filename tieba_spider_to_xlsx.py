# -*- coding: utf-8 -*-
import sys
import math
import urllib
import os
from lxml import etree
import requests
import json
from bs4 import BeautifulSoup
import xlsxwriter


def read_html(url):
    try:
        file1 = urllib.request.urlopen(url, timeout=5)
        data = file1.read()
        return data
    except:
        try:
            file1 = urllib.request.urlopen(url, timeout=5)
            data = file1.read()
            return data
        except:
            print('read_html error:'+str(url))
            return None


def scrapy(url):
    data = read_html(url)
    if data is not None:
        html = etree.HTML(data)

        # 帖子链接
        link = html.xpath("//a[@class='j_th_tit ']/@href")
        # 帖子数量
        post_num = int(html.xpath('//span[@class="red_text"]')[0].text)
        pages = math.ceil(post_num/50)
        return link, pages
    else:
        print('get link error:'+str(url))
        return None


def get_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
               'Connection': 'close'}
    try:
        data1 = requests.get(url, headers=headers, timeout=(3, 7))
        return data1
    except:
        try:
            data1 = requests.get(url, headers=headers, timeout=(3, 7))
            return data1
        except:
            print('get url error:'+str(url))
            return None


def test1(url, file, max_page, count, page_now, page_total):
    data1 = get_url(url)
    if data1 is not None:
        content = data1.text
        soup = BeautifulSoup(content, 'html.parser')
        excel_name = str(count)

        if soup.title.string != "贴吧404":
            limit = soup.find_all('span', class_='red')
            page_t = limit[1].get_text()
            page = min(int(page_t), int(max_page))

            if os.path.exists(file):
                wb1 = xlsxwriter.Workbook(file + '/' + excel_name + '.xlsx')
            else:
                os.makedirs(file)
                wb1 = xlsxwriter.Workbook(file + '/' + excel_name + '.xlsx')
            ws = wb1.add_worksheet(file)
            rnb = 0

            # 对于帖子的每一页
            for k in range(int(page)):
                url1 = url + "?pn=" + str(k + 1)
                print(url1+' total:'+str(int(page))+' now '+str(page_now)+' in '+str(page_total)+' pages')
                data1 = get_url(url)
                if data1 is not None:
                    content = data1.text
                    soup = BeautifulSoup(content, 'html.parser')

                    # 对于每一层楼
                    for post in soup.find_all('div', class_='l_post'):
                        # 找回复
                        try:
                            rep = post.find('div', class_='d_post_content')
                            postcontent = rep.get_text()
                        except:
                            print('未找到回复')
                            postcontent = None
                        # 找时间
                        try:
                            te = post.find_all('span', class_="tail-info")
                            posttime = te[-2].get_text() + te[-1].get_text()
                        except:
                            try:
                                jsonObject = json.loads(post.attrs['data-field'])
                                floornum = jsonObject['content']['post_no']
                                floortime = jsonObject['content']['date']
                                posttime = str(floornum)+'楼'+str(floortime)
                            except:
                                print('未找到时间')
                                posttime = None
                        # 找人
                        try:
                            # jsonObject = json.loads(post.attrs['data-field'])
                            # postname = jsonObject['author']['user_name']
                            pp = post.find('a', class_='p_author_name')
                            postname = pp.get_text()
                        except:
                            print('未找到人')
                            postname = None
                        if (postcontent is not None) and (posttime is not None) and (postname is not None):

                            ws.write(0, 3 * rnb, postcontent)
                            ws.write(0, 3 * rnb + 1, posttime)
                            ws.write(0, 3 * rnb + 2, postname)
                            rnb += 1
                        else:
                            print('post floor {} error:{}'.format(rnb+1, str(url)))
                else:
                    print('post page error:'+str(url))
            wb1.close()


if __name__ == "__main__":
    if len(sys.argv) == 4:
        name = sys.argv[1]
        file = sys.argv[2]
        max_page = sys.argv[3]
    elif len(sys.argv) == 3:
        name = sys.argv[1]
        file = sys.argv[2]
        max_page = 10000
    else:
        name = '柯南'
        file = 'kenan'
        max_page = 100

    x = urllib.request.quote(name)
    href, page_num = scrapy("https://tieba.baidu.com/f?kw="+x)
    max_page_num = min(page_num, 200)

    count = 1

    for j in range(0, max_page_num):
        x = urllib.request.quote(name)
        href, page_s = scrapy("https://tieba.baidu.com/f?kw="+x+"&pn="+str(j*50))
        if href is not None:
            # print('----post pages {}/{}----'.format(j+1, max_page_num))
            for i in href:
                path = "https://tieba.baidu.com"+i
                test1(path, file, max_page, count, j, max_page_num)
                count = count + 1
        else:
            print('href error')
