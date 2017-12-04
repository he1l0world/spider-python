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
        proxy = str(random.choice(proxy_ip))
        r = requests.get(url,timeout = 10 , headers = headers , proxies = dict(http = 'http://{}'.format(proxy)))
        #if(r.status_code != 200):
        #   print("wrong");
        r.raise_for_status()
        r.endcoding = 'utf-8'
        #print(r.text)
        return r.text
    except:
        return ""

def parse_html(id,url):
    count = 5
    html = 'https://mdskip.taobao.com/core/initItemDetail.htm?addressLevel=2&isAreaSell=false&service3C=false&cartEnable=true&queryMemberRight=true&isUseInventoryCenter=false&showShopProm=false&isForbidBuyItem=false&tryBeforeBuy=false&cachedTimestamp=1512371986997&isRegionLevel=false&tmallBuySupport=true&household=false&isPurchaseMallPage=false&isSecKill=false&isApparel=false&sellerPreview=false&offlineShop=false&itemId=' +str(id) + '&callback=setMdskip&timestamp=1512388710563&isg=null&isg2=Amhox9a2pi5mg4lmuy1et1hROV-6OdL1qzgX0SKZIOPefQjnyqGcK_79ASN2&ref=https%3A%2F%2Fs.taobao.com%2Fsearch%3Fq%3D%25E4%25B9%25A6%25E5%258C%2585%26imgfile%3D%26js%3D1%26stats_click%3Dsearch_radio_all%253A1%26initiative_id%3Dstaobaoz_20171119%26ie%3Dutf8'
    header = headers
    header['referer'] = 'https://detail.tmall.com/item.htm'
    header['cookie'] = 'miid=2204118637502781093; v=0; cna=OldwEsEx8ggCAXUg2BpcrJoP; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; UM_distinctid=15f8c5b57023a5-0160ece53b0bf5-1227170b-1fa400-15f8c5b5705492; tk_trace=oTRxOWSBNwn9dPy4KVJVbutfzK5InlkjwbWpxHegXyGxPdWTLVRjn23RuZzZtB1ZgD6Khe0jl%2BAoo68rryovRBE2Yp933GccTPwH%2FTbWVnqEfudSt0ozZPG%2BkA1iKeVv2L5C1tkul3c1pEAfoOzBoBsNsJySRNvOSY9xGDUNOPipFnPYpbkOlsF%2FySSuK1LjLRXwSVrAAJ6uhqKKgwAhm7Vn6J%2F%2BBQum9LSSkQ7juhP8Wptgb59VNPre3M56pSRUjc6yCmUNijDS8RYxfRd7QyT7lHjTOJ8LuMu9HsodGNX5qWeLi6%2FnMyd6UjDQfoo8Mzk%2F5Pd2L7%2FbC0IXdJfO; whl=-1%260%260%261510277548811; ucn=unshyun; _tb_token_=33e11e6d13736; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; linezing_session=NKYCLGnjBqZcbF5hZR80OFTY_1512388712170lXCt_5; uc1=cookie14=UoTdeYfCsXZFaA%3D%3D&lng=zh_CN&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&existShop=false&cookie21=Vq8l%2BKCLjhS4UhJVbhgU&tag=8&cookie15=VT5L2FSpMGV7TQ%3D%3D&pas=0; uc3=nk2=tPEAllpDUYwe5KgY&id2=UUBb2LhspNHhgw%3D%3D&vt3=F8dBzLQKZIXfZohL%2FCg%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; existShop=MTUxMjM4OTUyNg%3D%3D; lgc=%5Cu6700%5Cu7231%5Cu831C%5Cu831C1228; tracknick=%5Cu6700%5Cu7231%5Cu831C%5Cu831C1228; cookie2=3355e2a725b37da4b7c113f3def1f1f7; sg=880; mt=np=&ci=-1_0; cookie1=UIZs8ssf3EgnX%2BXL4c7N%2BeFC%2FglSJABncU4IIVYc8bs%3D; unb=2832844388; skt=ef36b8c0e19e72d3; t=7a6950203c53d620ab6f0c16c4928a6c; _cc_=Vq8l%2BKCLiw%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=%5Cu6700%5Cu7231%5Cu831C%5Cu831C1228; cookie17=UUBb2LhspNHhgw%3D%3D; isg=AlFRjLeH70XkdQCJ8OOVCXFHYFQrFtteav_eijPmPpgy2nEsew7VAP86CJjH'
    #html = url + str(id)
    #print(html)
    proxy = str(random.choice(proxy_ip))
    print(proxy)
    while count > 0:#尝试5次连接
        try:               #尝试用天猫网页来解析
            r = requests.get(html, timeout=10, headers=header, proxies =dict(http='http://{}'.format(proxy)))
            r.endcoding = 'utf-8'
            print("http://%s"%(proxy))
            print(r.text)
            return r.text
        except:            #尝试淘宝页面来解析
            count-=1
            print("wrong proxy %s"%(proxy))
    time.sleep(10)
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
            content = parse_html(q.get(),html)
            if (content != None):
                time.sleep(10)
            sale = re.findall(r'"sellCount":(.*?),',content)
            print(sale)
            #print(sales)
            info.append([price , title ,str(sale)])
            time.sleep(5)
            if(i > 3):
                break;
    #except:
        #print("")
def display(info):
    dislist = "{:4}\t{:4}\t{:4}\t{:4}"
    print(dislist.format("序号","价格","商品名称","销量","位置"))
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
            #continue;
    #display(info)
main()
