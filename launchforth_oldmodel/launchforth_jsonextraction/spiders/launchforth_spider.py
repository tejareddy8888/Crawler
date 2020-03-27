# -*- coding: utf-8 -*-
import scrapy
from json import loads,dump
from launchforth_jsonextraction.items import LaunchforthJsonextractionItem
import launchforth_jsonextraction.settings as crawling
import re
from datetime import datetime
from csv import DictWriter
from scrapy import Request
from scrapy import Spider


def extract_json(resp):
    return loads(resp.text.encode('utf-8'))

def jsonContentDateReplacer(v, j=None, k=None):
    """
    Recursive Timestamp Modifier from the dict input v 
    goes through every key of the v and if it finds a unreadable Datetime format , it will change it to readable format
    """
    if type(v) == dict:
        for key, val in v.items():
            jsonContentDateReplacer(val, v, key) 
        return
    if type(v) == list:
        for i in range(len(v)):
            jsonContentDateReplacer(v[i])
        return
    if type(v)!=str:
        return
    m = re.search('\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d', v)
    if m:
        j[k] = datetime.strptime(m.group(0), '%Y-%m-%dT%H:%M:%S')
    return 

class LaunchforthSpiderSpider(Spider):
    name = 'launchforth_spider'
    ID_key = ''
    def __init__(self,allowed_domains,start_urls,ID_key):
        self.allowed_domains = allowed_domains
        self.start_urls = start_urls
        self.ID_key = ID_key

    @classmethod
    def from_crawler(cls, crawler):
        allowed_domains = crawler.settings['DOMAIN']
        print(allowed_domains)
        start_urls = [crawler.settings['PREFIX']+ crawler.settings['MONGODB_COLLECTION'] + '/']
        ID_key = crawler.settings['ID_KEY']
        return cls(allowed_domains,start_urls,ID_key)

    def parse(self, response):
        self.logger.info("crawled " + response.url,)
        d = extract_json(response)
        jsonContentDateReplacer(d)
        results = d['results']
        # set primary Id for each content dict object. Then pack them as an Item to store in MongoDB
        for result in results:
            if self.ID_key in result:
                result[u'_id'] = result[self.ID_key]
        item = LaunchforthJsonextractionItem()
        item['content'] = results
        yield item
        # extract next url to crawl
        if 'next' in d and d['next']:
            yield Request(url=d['next'], callback=self.parse)
    
"""
class LaunchforthSpiderSpider(scrapy.Spider):
    name = 'launchforth_spider'
    allowed_domains = ['launchforth.io']
    prefix = f'https://launchforth.io/api/v3/'
    i = 0
    def start_requests(self):
        '''As per Scrapy Framework you can start with either start_urls or 
            start_requests is the base function to start Spider to crawl in
            Scrapy framework like main function'''
        
        #As of now this is built to scrape only the input Project Category
        self.logger.info("Started to Scrape the website with Category"+self.projects_category)
        yield scrapy.Request(url= self.prefix +'content/?content_type_name=project&category={0}'.format(self.projects_category), callback=self.parse)

    def parse(self, response):
        self.logger.info("Fetched the projects under above category")

        temp = extract_json(response)   

        item = LaunchforthJsonextractionItem()
        item['content'] = temp['results']

        for i in range(0,1):
            link = self.prefix+'project/'+str(item['content'][i]['object_id'])+'/'
            self.logger.info("extracting project"+str(i))
            print(item['content'][i]['object_id'])
            print(link)
            yield scrapy.Request(url=link,callback=self.parse_individualProject,meta={'href':link})

    def parse_individualProject(self,response):
        link = response.request.meta['href']
        self.logger.info("extracted project details")
        temp = extract_json(response)
        jsonContentDateReplacer(temp)
        self.logger.info("Formatted the data received")
        Data = {
        'Content': temp['description'],
        'Project_Title': temp['title'],
        'Discussion_id' : temp['discussion_topic'],
        'Creation_date': str(temp['created']),
        'Last_Updated_data' : str(temp['updated']),
        'Summary': temp['title']
        }
        #print(Data)
        if self.i == 0 :
            with open('data.csv', 'w+') as csv_file:  
                w =  DictWriter(csv_file,fieldnames=Data.keys())
                w.writeheader()
                w.writerow(Data)
                self.i+=1
        else:
            with open('data.csv', 'a+') as csv_file:  
                w =  DictWriter(csv_file,fieldnames=Data.keys())
                w.writerow(Data)       
        link = link + str('timeline/')
        yield  scrapy.Request(url=link,callback=self.parse_individualTimeline,meta={'href':link})

    def parse_individualTimeline(self,response):
        link = response.request.meta['href']
        self.logger.info("extracted project timelines")
        temp = extract_json(response)
        jsonContentDateReplacer(temp)
        print(temp)
        for i in range(0,temp['count']):
            Data= {
                'Timeline' : temp['results'][i].get('created'),
                'Announcement' : temp['results'][i].get('is_announcement'),
                'TimelineDetails' : temp['results'][i].get('snippet'),
            }
            with open('data.csv', 'a+') as csv_file:  
                w =  DictWriter(csv_file,fieldnames=Data.keys())
                w.writerow(Data)          
        self.logger.info("Formatted the data received")
        yield
        {
                'Timeline' : temp['results'][i].get('created'),
                'Announcement' : temp['results'][i].get('is_announcement'),
                'TimelineDetails' : temp['results'][i].get('snippet'),            
        }
    """