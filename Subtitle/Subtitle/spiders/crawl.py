import scrapy
#from spider.lib import Interface_Crawl
#import interface_crawl
import logging
import sys
from Subtitle.settings import USER_AGENT_LIST
from Subtitle.settings import PROXIES
from scrapy import Selector
from Subtitle.items import SubtitleItem
import random
import os

#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(level=logging.INFO)
logging.info('sys.path = {}'.format(sys.path))

class Crawl(scrapy.Spider):
    '''
    using default start_request method and inherit from the Interface_Crawl
    '''
    name = 'subku'
    #allowed_domains =  ['http://www.subku.net']
    start_urls = 'http://www.subku.net/dld/1.html'
    #total_num = 110390  #This is the total num of links
    total_num = 10 # This is test num
    page_num = 1
    def __init__(self ):
        pass
    def start_requests(self):
        usr_agent = self.Random_Agent()
        logging.info('usr_agent = {}'.format(usr_agent))

        proxy = self.Random_Proxy()
        yield scrapy.Request(self.start_urls, headers = usr_agent )
        #yield scrapy.Request(self.start_urls, headers = usr_agent, )
    def parse(self, response):
        item = SubtitleItem()
        usr_agent = self.Random_Agent()
        proxy = self.Random_Proxy()


        url = response.xpath('//li/a/@href').extract()
        print(url[0])
        item['url'] = url[0]
        item['page_num'] = self.page_num
        yield item
        if self.page_num <= self.total_num - 1:
            self.page_num += 1
            next_url = 'http://www.subku.net/dld/' + str(self.page_num) + '.html'
            yield scrapy.Request(next_url,headers = usr_agent)
    def Random_Proxy(self):
        return 'http://'+random.choice(PROXIES)
    def Random_Agent(self):
        return {'User-Agent': random.choice(USER_AGENT_LIST)}
