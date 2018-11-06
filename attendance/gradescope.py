import re
from bs4 import BeautifulSoup as bs
import requests
import time
from tkinter import messagebox
import tkinter as tk


def main ():
    filename = 'cookies.txt'
    try:
        course = int(input("Pls enter which course you taking(number) eg: 8 or 11\n"))
    except ValueError:
        print("Pls enter valid number")
        exit()
    cookies = read_cookies(filename)
    check = input('Pls Enter which attendance you wanna: eg: Attendance 10 or Section Attendance 2\n')


    url_8am = 'https://www.gradescope.com/courses/21587'
    url_11am = 'https://www.gradescope.com/courses/21588'
    url = ''
    if course == 8:
        url = url_8am
    elif course == 11:
        url = url_11am
    else:
        print('Pls choose 8 or 11')
        exit(0)

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

    header['Cookie'] = cookies[:len(cookies) -1]  # python read file will automatic add a Newline('\x0a') at the end of the string

    if not check_attendance(url, header):
        # test if the connect is right
        print('connect failed')
    while True:
        if check_attendance(url, header, check):
            print(time.asctime(time.localtime(time.time())) ,' Success find the',check)
            pop_notification()
            exit(0)
        else:
            print(time.asctime(time.localtime(time.time())),' Failed to find the', check)
        time.sleep(9)


#def get_window():
#    return window.win_screenwidth(), window.win_screenheight()
def read_cookies(filename):
    try :
        cookies = open(filename, "r")
    except:
        print("open cookies.txt file failed, Pls write your own cookies into cookies.txt")
        exit()
    cookie = cookies.read()
    cookies.close()
    return cookie
def pop_notification():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title = 'New Attendance Question!', message = 'Find a new Attendance question')



def check_attendance(url, header, check = 'Attendance 1'):
    try:
        s = requests.session()
        re = s.get(url, headers = header)
    except:
        print("request failed pls contact me!")
        exit()
    #cookie = cookiejar.CookieJar()
    #cookie_support = request.HTTPCookieProcessor(cookie)
    #opener = request.build_opener(cookie_support)
    #res = opener.open(html)
    #res = res.read().decode('utf-8')
    re.encode = 'utf-8'
    html = re.text
    soup = bs(html,'html.parser')
    for items in soup.find_all('a'):
        if check in items:
            return True
    return False

main()

#<a aria-label="View Section Attendance 3" href="/courses/21587/assignments/99826/submissions/9117732">Section Attendance 3</a>
