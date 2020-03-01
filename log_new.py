#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib
#import os
from lxml import etree
import requests
import re
from bs4 import BeautifulSoup
import time
#import pandas as pd
#import xlsxwriter
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
#session = requests.session()

#wb = xlwt.Workbook(encoding='utf-8')

#requests.adapters.DEFAULT_RETRIES = 5

##行序号
#cnb = 0
#num = 0

def read_HTML(url):
    file = urllib.request.urlopen(url)
    data = file.read()
    return data


#def login():
#    login_url = "https://tieba.baidu.com/index.html"
#    driver = webdriver.Firefox(executable_path='C:\\Users\wyj\Desktop\geckodriver')
#    driver.get(login_url)
#    time.sleep(0.16)
#    element = driver.find_element_by_link_text("登录")
#    element.click()
#    time.sleep(1)
#    element = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__footerULoginBtn"]')
#    element.click()
#    element = driver.find_element_by_id("TANGRAM__PSP_10__userName").send_keys("360341083@qq.com")
#    element = driver.find_element_by_id("TANGRAM__PSP_10__password").send_keys("1996wyjx")
#    element = driver.find_element_by_id("TANGRAM__PSP_10__submit").click()
#    time.sleep(1)
#    mode = input('需要二代验证,输入验证方式的序号\n1.手机验证\n2.密保邮箱验证\n请输入验证方式:')
#
#    driver.find_element_by_xpath('//*[@id="TANGRAM__25__button_send_mobile"]').click()
#    vcode = input('请输入验证码:')
#    driver.find_element_by_xpath('//*[@id="TANGRAM__25__input_vcode"]').send_keys(vcode)
#    driver.find_element_by_xpath('//*[@id="TANGRAM__25__button_submit"]').click()
#    time.sleep(2.5)
#    return driver


#def save(dt):
#    with open("C:\\Users\wyj\Desktop\data.txt", "w") as f:
#        f.writelines(dt)
#
#
#def read():
#    with open("C:\\Users\wyj\Desktop\data.txt", "r") as f:
#        data = f.readlines()
#        return data

def scrapy(url):
    #url="https://tieba.baidu.com/f?kw="+x
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


#def test2(driver):
#    url = "https://tieba.baidu.com/p/6103073155"
#    driver.get(url)
#    time.sleep(0.16)
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # element0 = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/a')
    # if element0.is_displayed():
    #     ele0.click()
    # data = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/ul/li[1]/div/span')
    # print(data.text)
    # for i in soup.find_all('span', class_='lzl_content_main'):
    #     print(i.text)


#def auto_down(url,filename,i):
#    try:
#        print(url)
#        maxtrytime = 10
#        for trys in range(maxtrytime):
#            try:
#                urllib.request.urlretrieve(url, filename)
#                break
#            except urllib.error.URLError:
#                if trys < maxtrytime - 1:
#                    time.sleep(10)
#                    continue
#                else:
#                    break
#    except urllib.request.ContentTooShortError:
#        i += 1
#        if i < 3:
#            auto_down(url,filename,i)
#        else:
#            print('fail')
#



#def getImage(html, path):
#    reg = r'src="(.+?)"'  # 正则表达式，得到图片地址
#    imgre = re.compile(reg)  # re.compile() 可以把正则表达式编译成一个正则表达式对象.  # python3
#    imglist = re.findall(imgre, html)  # re.findall() 方法读取html 中包含 imgre（正则表达式）的数据
#    # 把筛选的图片地址通过for循环遍历并保存到本地
#    # 核心是urllib.request.urlretrieve()方法,直接将远程数据下载到本地，图片通过x依次递增命名
#    global num
#    for imgurl in imglist:
#        if re.match("https",imgurl) != None:
#            auto_down(imgurl, path+'\%s.jpg' % num, 0)
#        else:
#            if re.match('http',imgurl) != None:
#                auto_down(imgurl, path + '\%s.jpg' % num, 0)
#            else:
#                imgurl = "https:"+imgurl
#                auto_down(imgurl, path + '\%s.jpg' % num, 0)
#        num += 1
#    return imglist

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
    #url='https://tieba.baidu.com/p/6521477887'
    #global num
    #global cnb
    ##列序号
    #rnb = 0
    #rp = []
    #rpt = []
    #rpu = []
    maxtrytime = 5
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
    time.sleep(0.3)
    content = data1.text
    soup = BeautifulSoup(content, 'html.parser')
    #excelname = findname(soup)
    #if excelname==None:
    #    excelname='error'
    #if os.path.exists('/Users/hugh/Documents/socialnetwork/spider/kenan'):
    #    wb1 = xlsxwriter.Workbook("/Users/hugh/Documents/socialnetwork/spider/kenan/" + excelname + '.xlsx')
    #else:
    #    os.makedirs('/Users/hugh/Documents/socialnetwork/spider/kenan')
    #    wb1 = xlsxwriter.Workbook("/Users/hugh/Documents/socialnetwork/spider/kenan/" + excelname + '.xlsx')
    #ws = wb1.add_worksheet('cosplay')
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
            ##找到每一个帖子下面的回复
            # dt = soup.find_all('div', class_="d_post_content j_d_post_content")
            # for i in dt:
            #     rp.append(i.get_text())
            #     # print(i.get_text())
            # ##找到回复的时间
            # tm = soup.find_all('span', class_="tail-info")
            # for i in tm:
            #     rpt.append(i.get_text())
            #     # print(i.get_text())
            #     # print(i.get_text())
            # ##找到发回复的人
            # rpp = soup.find_all('a', class_='p_author_name j_user_card')
            # for i in rpp:
            #     # print(i.get_text())
            #     rpu.append(i.get_text())
            # # print(len(rp))
            # # print(len(rpt))
            # # print(len(rpu))
            ##找到帖子名称
            #nname = findname(soup)
            
            for i in soup.find_all('div',class_='l_post l_post_bright j_l_post clearfix '):
                #对于每一个回帖
                # ##找到回复
                # print(str(i))
                username=' '
                floornum=' '
                posttime=' '
                postcontent=' '
                
                rep = i.find('div', class_='d_post_content j_d_post_content ')
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
                
                #if len(te) == 3:
                    # print(te.get_text())
                    # print(te[2].get_text())
                    #ws.write(0, 3*rnb+1, te[1].get_text()+te[2].get_text())
                #else:
                    #if len(te) == 2:
                        #ws.write(0, 3 * rnb + 1, te[0].get_text() + te[1].get_text())
                    #else:
                    #    data = requests.get(url1,headers=headers)
                    #    content = data.text
                    #    soup = BeautifulSoup(content, 'html.parser')
                    #    soup.find_all('span', class_="tail-info")
                    #    if len(te) == 3:
                    #        # print(te.get_text())
                    #        # print(te[2].get_text())
                    #        ws.write(0, 3 * rnb + 1, te[1].get_text() + te[2].get_text())
                    #    else:
                    #        if len(te) == 2:
                    #            ws.write(0, 3 * rnb + 1, te[0].get_text() + te[1].get_text())

                    # print(te.get_text())
                    # print(te[1].get_text())

                #     ws.write(cnb,rnb,te)
                ##找人
                pp = i.find('a', class_='p_author_name')
                if pp != None:
                    username=pp.get_text()
                results_list.append(username)
                results_list.append(floornum)
                results_list.append(posttime)
                results_list.append(postcontent)
    return results_list
                        
                        # print(pp.get_text())
                        #ws.write(0, 3 * rnb + 2, pp.get_text())
                    #rnb+=1
    #wb1.close()
    #return None
#                    else:
#                        pp = i.find('a', class_='p_author_name j_user_card vip_red')
#                        if pp != None:
#                            # print(pp.get_text())
#                            ws.write(0, 3 * rnb + 2, pp.get_text())
#                        else:
#                            pp = i.find('a', class_='p_author_name sign_highlight j_user_card')
#                            if pp != None:
#                                # print(pp.get_text())
#                                ws.write(0, 3 * rnb + 2, pp.get_text())
#                            else:
#                                pp = i.find('a', class_='p_author_name sign_highlight j_user_card vip_red')
#                                if pp!=None:
#                                    # print(pp.get_text())
#                                    ws.write(0, 3 * rnb + 2, pp.get_text())
                    # print(pp.get_text())
                    # print(te[1].get_text())
#                    for j in i.find_all('div', class_='d_post_content j_d_post_content '):
#                        if len(te) == 3:
#                            if os.path.exists('F:\QQdownload\\360341083\FileRecv\柯南\\' + nname+'\\' + pp.get_text() + '\\' + te[2].get_text().split(' ')[0]):
#                                getImage(str(j), 'F:\QQdownload\\360341083\FileRecv\柯南\\'+ nname+'\\' +pp.get_text() +'\\' + te[2].get_text().split(' ')[0])
#                            else:
#                                os.makedirs('F:\QQdownload\\360341083\FileRecv\柯南\\' + nname +'\\'+ pp.get_text() + '\\' + te[2].get_text().split(' ')[0])
#                                getImage(str(j), 'F:\QQdownload\\360341083\FileRecv\柯南\\'+ nname+'\\' + pp.get_text() +'\\' + te[2].get_text().split(' ')[0])
#                        else:
#                            if os.path.exists('F:\QQdownload\\360341083\FileRecv\柯南\\' + nname+'\\' + pp.get_text() + '\\' + te[1].get_text().split(' ')[0]):
#                                getImage(str(j), 'F:\QQdownload\\360341083\FileRecv\柯南\\'+nname+'\\'+ pp.get_text() +'\\' + te[1].get_text().split(' ')[0])
#                            else:
#                                os.makedirs('F:\QQdownload\\360341083\FileRecv\柯南\\' +nname+'\\'+ pp.get_text() + '\\' + te[1].get_text().split(' ')[0])
#                                getImage(str(j), 'F:\QQdownload\\360341083\FileRecv\柯南\\'+nname+'\\'+ pp.get_text() +'\\' + te[1].get_text().split(' ')[0])
#                        num += 1

    # for i in range(len(rp)):
    #     ws.write(cnb, 3*i+2, rp[i])
    #     ws.write(cnb, 3*i+3, rpt[i])
    #     ws.write(cnb, 3*i+4, rpu[i])


    ##找到帖子中的恢复的回复
    # rp = soup.find_all('span', class_="lzl_content_main")
    # for i in rp:
    #     print(rp.select('span').get_text())
    # data = read_HTML(url)
    # html = etree.HTML(data)
    # beta = html.xpath("//div[@class='d_post_content j_d_post_content ']")
    # dat = html.xpath("//span[@class='lzl_content_main']")
    # for i in dat:
    #     print(i.text)
    # for i in beta:
    #     # s = i.text.encode("gb18030")
    #     # chardet.detect(i.text)
    #     # print(i.text)
    #     print(0)


def text(url):
    for i in url:
        gurl = "https://tieba.baidu.com"+i
        data = read_HTML(gurl)
        html = etree.HTML(data)
        beta = html.xpath("//div[@class='d_post_content j_d_post_content ']")
        for i in beta:
            print(i.text)


if __name__ == "__main__":
#    x = urllib.request.quote("柯南")
#    href,pags = scrapy("https://tieba.baidu.com/f?kw="+x)
    filename = 'data.csv'
    for j in range(0, 2):
        x = urllib.request.quote("柯南")
        href,pgs = scrapy("https://tieba.baidu.com/f?kw="+x+"&pn="+str(j*50))
        for i in href:
            path = "https://tieba.baidu.com"+i
            #path='https://tieba.baidu.com/p/6521477887'
            results=test1(path)
            with open(filename, 'a') as file_object:
                for content in results:
                    if content!=results[-1]:
                        file_object.write(content)
                        file_object.write(',')
                    else:
                        file_object.write(content)
                        file_object.write('\n')
            
