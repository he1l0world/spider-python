#!/usr/bin/env python3.5
# coding=utf-8
import requests
import time
import random
import re
import os
import threading
import urllib
import queue



q = queue.Queue()
#"confirmGoodsCount":634,"soldTotalCount":995


#https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=44444180170&sellerId=94445060&modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,upp,activity,fqg,zjys,amountRestriction,couponActivity,soldQuantity,originalPrice,tradeContract&callback=onSibRequestSuccess



#https://mdskip.taobao.com/core/initItemDetail.htm?isForbidBuyItem=false&tmallBuySupport=true&addressLevel=2&showShopProm=false&isRegionLevel=false&queryMemberRight=true&offlineShop=false&isPurchaseMallPage=false&isAreaSell=false&isSecKill=false&isUseInventoryCenter=false&cartEnable=true&cachedTimestamp=1511050188384&sellerPreview=false&household=false&isApparel=false&itemId=38922791907&tryBeforeBuy=false&service3C=false&callback=setMdskip&timestamp=1511102706195&isg=null&isg2=AjU14Go8g-W75OShTq5bOLUCRLgvGveqtqt61rdZnKx-jlWAfwL5lENOrGRD&ref=https%3A%2F%2Fs.taobao.com%2Fsearch%3Fq%3D%25E4%25B9%25A6%25E5%258C%2585%26imgfile%3D%26js%3D1%26stats_click%3Dsearch_radio_all%253A1%26initiative_id%3Dstaobaoz_20171119%26ie%3Dutf8


#https://mdskip.taobao.com/initItemDetail.htm?&itemId=389227919077



#<em class="J_ReviewsCount" style="display: inline;">333245</em>
#<label for="J_RateWithAppend1510277551863">追评 (13426)</label>
#<label for="J_RateWithPicture1510277551863">图片 (34858)</label>

#http://ip.chinaz.com/getip.aspx
headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}
proxy_ip = []
def get_proxy():#将所有的有效代理ip存储起来
    #content
    with open('/home/dawson_chen/programming/github/proxy_pool/log/proxy_check.log') as f:#将每一个可以用的ip存在列表中
        for lines in f:
            line = str(lines)
            #print(line.split(' ')[-1] == 'pass\n')
            if(line.split(' ')[-1] == 'pass\n'):#每一行最后都有一个换行符
                line = str(line.split(' ')[-3])
                #print(line)
                proxy_ip.append(line)
                #lprint(line.split(' ')[-3])

    f.close()


def delete_proxy(proxy):
    #requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
    proxy_ip.remove(proxy)


def gethtml(url):
    try:
        proxy = str(random.choice(proxy_ip))[2:-1]
        r = requests.get(url,timeout = 10 , headers = headers , proxies = dict(http = 'http://{}'.format(proxy)))
        #if(r.status_code != 200):
        #   print("wrong");
        r.raise_for_status()
        r.endcoding = 'utf-8'
        #print(r.text)
        return r.text
    except:
        return ""

def parse_html(id):
    count = 5
    html = 'https://mdskip.taobao.com/core/initItemDetail.htm?&itemId='+str(id)
    #html = url + str(id)
    print(html)
    proxy = str(random.choice(proxy_ip))
    print(proxy)
    while count > 0:#尝试5次连接
        try:               #尝试用天猫网页来解析
            r = requests.get(html, timeout=10, headers=headers, proxies =dict(http='http://{}'.format(proxy)))
            r.endcoding = 'utf-8'
            print("http://%s"%(proxy))
            print(r.text)
            return r.text
        except:            #尝试淘宝页面来解析
            count-=1
            print("wrong URL %s"%(html))
    delete_proxy(proxy)
    return None
def parse(info,html):
    #try:
        plt = re.findall(r'\"view_price\"\:\".*?\"',html)
        tlt = re.findall(r'\"raw_title\"\:\".*?\"',html)
        id = re.findall(r'\"nid\"\:\".*?\"',html)
        t = 'https://detail.tmall.com/item.htm?id='
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            it = eval(id[i].split(':')[1])
            ot = t+str([it])
            q.put(it) #insert the url to queue
            #print(it)
            parse_html(q.get())
            info.append([price , title ,ot])
            time.sleep(5)
            if(i > 3):
                break;
    #except:
        #print("")
def display(info):
    dislist = "{:4}\t{:4}\t{:4}\t{:4}"
    print(dislist.format("序号","价格","商品名称","URL"))
    count = 0;
    for g in info:
        count+=1
        print(dislist.format(count , g[0] , g[1],g[2]))
def main():
    goods = input('请输入查询商品名称：  ')
    depth = input('请输入查询页数：    ')
    start_url = 'https://s.taobao.com/search?q='+str(goods)
    info = []
    get_proxy()
    #print(proxy_ip)
    for i in range (int(depth)):
        try:
            url = start_url+'&s='+str(44*i)
            html = gethtml(url)
            parse(info,html)
        except:
            print('web wrong %s' %url)
            continue;
    #display(info)
main()
