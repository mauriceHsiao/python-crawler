#coding:utf-8
import requests,re,sys
import pypyodbc  ##連線資料庫
from bs4 import BeautifulSoup

conn = pypyodbc.connect("DRIVER={SQL Server};SERVER=127.0.0.1,14333;DATABASE=News;")
cursor = conn.cursor()
    
def news_content(links):
    global sql
    sql = "insert into [News].[dbo].[chinatimes_news] values("
    result = requests.get(links)
    result.encoding = 'utf-8'
    soup = BeautifulSoup(result.text,"html.parser")

    #title
    retitle = r' |\n'
    title = re.sub(retitle,r'',str(soup.find('hgroup').find('h1').text))
    with open('news_log.txt','a') as f:
        f.write("title="+str(title).encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding)+"\n")
    sql = sql + "'" + str(title) + "',"

    #time
    retime = r"(\d{4}年.+月.+日.+)</time>"
    time = re.findall(retime,str(soup.find('article').find('time')))[0]
    with open('news_log.txt','a') as f:
        f.write("time="+str(time)+"\n")
    sql = sql + "'" + str(time) + "',"

    #content
    re1 = r'<p>|</p>'
    contentli = []
    sql = sql  + "'"
    for i in soup.find('article').findAll('p'):
        content = re.sub(re1,r'',(str(i)))
        contentli.append(content)

    with open('news_log.txt','a') as f:
        f.write("content=")
        for con in contentli[:-1]:
            f.write(str(con).encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding))
            sql = sql + str(con)
        f.write("\n")
    sql = sql + "',"

    #publisher
    sql = sql + "'" + str(contentli[-1]) + "',"
    with open('news_log.txt','a') as f:
        f.write("publisher="+str(contentli[-1])+"\n")
        
    #img url
    try:
        reimg = r'<img src="(.+)"><span></span>'
        img = re.findall(reimg,str(soup.find('figure').find('a').find('img')))[0]
        with open('news_log.txt','a') as f:
            f.write("img url="+str(img)+"\n")
        sql = sql  + "'"+ str(img) + "',"
    except:
        with open('news_log.txt','a') as f:
            f.write("No img url. \n")
        sql = sql  + "'',"
        
    #img title
    try:
        reimgtitle = r'title="(.+)">'
        img_title = re.findall(reimgtitle,str(soup.find('figure').find('a')))[0]
        with open('news_log.txt','a') as f:
            f.write("img title="+str(img_title)+"\n")
        sql = sql  + "'" + str(img_title).encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding) + "',"
    except:
        with open('news_log.txt','a') as f:
            f.write("No img title. \n")
        sql = sql  + "'',"

    #link
    sql = sql  + "'" + str(links) + "')"
    with open('news_log.txt','a') as f:
        f.write("link="+str(links)+"\n")
    
    #sql 
    with open('news_log.txt','a') as f:
        f.write("sql="+str(sql).encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding)+"\n")
        
    try:
        cursor.execute(sql)
        conn.commit()
        with open('news_log.txt','a') as f:
            f.write("sql commit sucessfull\n")
    except Exception as e:
        with open('news_log.txt','a') as f:
            f.write("sql error="+str(e)+"\n")
    

