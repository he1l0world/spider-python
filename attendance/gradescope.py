import re
from bs4 import BeautifulSoup as bs
import requests
import time
from tkinter import messagebox
import tkinter as tk


def main ():
    filename = 'cookies.txt'
    cookies = read_cookies(filename)
    check = input('Pls Enter your check attendance: ')
    url = 'https://www.gradescope.com/courses/21587'
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.gradescope.com',
            'Referer': 'https://www.gradescope.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': '''Mozilla/5.0 (Macintosh'; 'Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36''',
            }

    header['Cookie'] = '_ga=GA1.2.1141250143.1534819808; signed_token=b2F3VlB0RVJtN1VucUhVUHZWcXFyZEt5SjdVYUdOU21qVHlITStidXpKTT0tLUxnY200U2c5MnMybVJzbVFMM3BUYXc9PQ%3D%3D--836f6c0f9343a41d90e28a9d138a42e0a719c295; _gid=GA1.2.157058492.1537208283; _gradescope_session=L0JNemtFdmZ4MnpzRVhjL3BVSndON1pIUzBKWkc2cDJqeUxlUkJ2ZDBVOWZjeHBBSWpRZjFrMXJyeE5CdWNhdDRUcDAxaHVBQUhTWlo4OUdYOStNSXRoN0pwcDZTSVVQcUZSYjJ6Mzhyemdpd2tja0REZ2k2cnp6WkFPZGp4Qm42Nmx5b2VucDJHTUUyb3AyckxXYUNYRE8rN1Jhb3A4RlZ0RU9oSzdHZzJHQThMa3pOSExiVndWNm1NdU5GaVJqZXlBSVZZQ2Fzb0xSYm5rOHlsMFRlSWg0TXM0dTR0UStjaWw3T2QvbWcxcE9tRjhHTWV1QldSRHZZUEQrbEViaFZXVjMwT0dPK29wNU8vRjFSVGJGdjZnVVlzeHpDeStPK3c5TUhucWxzci9ESlViWSsyQ2k1MkdRcHdjRFFQUnhMVEVSSnNPR1NpdjExNlZXVUJZU0hwL3V2OWpyZ0VXSWQwUnc3SXF2TDI0PS0tb0pVWWdoU3g3cmx3SXRaQSsrRzdlZz09--aedf694a963a41ea333d137f153d59beea1d3741'

    while True:
        if check_attendance(url, header, check):
            print(time.asctime(time.localtime(time.time())) ,' Success find the',check)
            pop_notification()
            exit(0)
        else:
            print(time.asctime(time.localtime(time.time())),' Failed to find the', check)
        time.sleep(60)


#def get_window():
#    return window.win_screenwidth(), window.win_screenheight()
def read_cookies(filename):
    pass
def pop_notification():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title = 'New Attendance Question!', message = 'Find a new Attendance question')



def check_attendance(url, header, check):
    s = requests.session()
    re = s.get(url, headers = header)
    #cookie = cookiejar.CookieJar()
    #cookie_support = request.HTTPCookieProcessor(cookie)
    #opener = request.build_opener(cookie_support)
    #res = opener.open(html)
    #res = res.read().decode('utf-8')
    re.encode = 'utf-8'
    html = re.text
    soup = bs(html,'lxml')
    for items in soup.find_all('a'):
        if check in items:
            return True
    return False

main()

#<a aria-label="View Section Attendance 3" href="/courses/21587/assignments/99826/submissions/9117732">Section Attendance 3</a>
