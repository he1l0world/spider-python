import re
import requests
import xlsxwriter
import string
import threading
import time
from bs4 import BeautifulSoup
from xlrd import open_workbook

times = 0
def error(i):
    with open('/home/dawson_chen/error.txt','a') as f:
        f.write("error question:"+str(i))
        f.close()
def writefile(info):
    workbook = xlsxwriter.Workbook('/home/dawson_chen/spider.xlsx')
    worksheet = workbook.add_worksheet()
    row = 1
    for each in (info):
        worksheet.write(row, 1, each[0])
        worksheet.write(row, 2 ,each[1])
        worksheet.write(row, 3, each[2])
        row += 1
    workbook.close()
info = []
def do_something():
    url = 'https://www.diandianwen.com/ask/initAskDetail/'
    headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}
    global info
    #i = depth
    for i in range (1,18091):
        try:
            html = url + str(i)
            a = ''
            b = ''
            c = ''
            r = requests.get(html, timeout=10, headers=headers)
            soup = BeautifulSoup(r.text,'lxml')
            a = str(soup.find_all('span',attrs="adop-date"))
            for child in soup.find_all('div', attrs ="adop-answer"):
                b +=str(child.find_all('span'))
                if(len(b) == 0):
                    b += str(child.find_all('p'))
            for child in soup.find_all('div',attrs = "answ-text"):
                b += str(child.find_all('p'))
            #print(b)
            #print(type(b))
            c = str(soup('title'))
            a = re.findall(r'<span class="adop-date">(.*).0</span>',a)
            answer = re.findall(r'>(.*?)</span>',b)
            #print(type(answer))
            if (answer == []):
                answer = re.findall(r'>[&nbsp;]{0,}(.*?)[&nbsp;]{0,}</p>',b)
            if(answer == []):
                b = ''
                for child in soup.find_all('div' ,attrs="adop-answer"):
                      b+=str(child.find_all('p'))
                answer = re.findall(r'>(.*?)</span>', b)
                # print(type(answer))
                if (answer == []):
                    answer = re.findall(r'>[&nbsp;]{0,}(.*?)[&nbsp;]{0,}</p>', b)
            c = re.findall(r'<title>(.*?)- 点点问税</title>',c)
            tim = ''.join(a)
            answer = ''.join(answer)
            question = ''.join(c)
            print("问题："+str(i))
            print(tim)
            print(question)
            print(answer)
            info.append([question , answer ,tim])
            #time.sleep(1)
            #print (info)
        except Exception as e:
            print (e)
            print("error question:"+str(i))
            error(i)
    writefile(info)
do_something()
