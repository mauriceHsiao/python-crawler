#coding:utf-8
import requests,re,time,random,news_chinatimes as news
import pypyodbc  ##連線資料庫
from bs4 import BeautifulSoup

def get_url(links):
    url_list=[]
    result = requests.get(links)
    result.encoding = 'utf-8'
    soup = BeautifulSoup(result.text,"html.parser")

    for i in range(30):
        retime = r'<time datetime="(.+)">.+</time>'
        posttime = re.findall(retime,str(soup.findAll('time')[i]))[0] 
        if posttime[:10] == "2018-01-29":
            print(posttime)

            #url
            reurl = r'<a href="(.+)">'
            url = re.findall(reurl,str(soup.findAll('h2')[i]))[0]
            print(url)
            news.news_content(url)
            
##            #title
##            title = soup.findAll('h2')[i].text
##            print(title)
            
        time.sleep(random.uniform(0.5, 2.9))
        
#get_url("http://www.chinatimes.com/money/industry?page=3")

for l in range(1,11):
    print("http://www.chinatimes.com/money/industry?page="+str(l))
    get_url("http://www.chinatimes.com/money/industry?page="+str(l))
    time.sleep(random.uniform(2.0, 4.9))
print("finish")

