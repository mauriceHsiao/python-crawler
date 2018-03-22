#coding:utf-8
import requests,re,time
import pypyodbc  ##連線資料庫
from bs4 import BeautifulSoup

def get_url(links):
    url_list=[]
    result = requests.get(links)
    result.encoding = 'utf-8'
    soup = BeautifulSoup(result.text,"html.parser")
    re2 = r'<a href="(.+)"><span class="th-underline">'
    firsturl = re.findall(re2,str(soup.find('div',{'class','grid@tl+__cell col-8-of-12@tl col-11-of-15@d flex-1'})))

    re1 = r'<a class="o-hit__link" href="(.+)">'
    url_list = re.findall(re1,str(soup.find('div',{'class','grid@tl+__cell col-8-of-12@tl col-11-of-15@d flex-1'})))
    url_list.insert(0,firsturl[0])
    print(url_list)

get_url("https://chinese.engadget.com/topics/industry-news/page/1/")
#get_url("https://udn.com/news/get_article/3/2/6644/7241")

#for l in range(2,11):
    #print("https://udn.com/news/get_article/"+str(l)+"/2/6644/7241")
    #get_url("https://udn.com/news/get_article/"+str(l)+"/2/6644/7241")
    #time.sleep(1.8)
print("finish")

