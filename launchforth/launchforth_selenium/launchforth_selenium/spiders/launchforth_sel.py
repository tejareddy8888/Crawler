# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from scrapy.selector import Selector
from launchforth_selenium.items import LaunchforthSeleniumItem
import json

class LaunchforthSelSpider(scrapy.Spider):
    name = 'launchforth_sel'
    allowed_domains = ['launchforth.io']
    start_urls = ['https://www.launchforth.io/']
    item = LaunchforthSeleniumItem()
    datadict = {}
    i = 0 

    def __init__(self):
        fopt = Options()
        fopt.headless=False
        driver = webdriver.Firefox(executable_path="geckodriver.exe",options=fopt)
        driver.get('https://www.launchforth.io/')

        driver.implicitly_wait(5)

        project_btn = driver.find_element_by_xpath("//span[@class='label' and contains(text(),'Projects')]")
        project_btn.click()

        driver.implicitly_wait(5)

        category = 'Human Machine Interface'

        category_btn = driver.find_element_by_xpath("//a[@class='ui suibutton' and contains(text(),'"+category+"')]")
        category_btn.click()

        driver.implicitly_wait(2)

        print(driver.find_element_by_class_name("page-header__title").text)

        self.html = driver.page_source
        i=0
        self.datadict['Project'] = {'ID':[]}
        self.datadict['Project'] = {'Name':[]}
        for resp in driver.find_elements_by_xpath("//*[@class='grid__content__item']/div/h2"):
            i=i+1
            self.datadict['Project'] = {'i':{}}
            self.datadict['Project'][i] = {'Name' : resp.text}
        for i in range(1,5):
            project_element = driver.find_element_by_xpath("//*[@class='grid__content__item']["+str(i)+"]")
            project_element.click()
            driver.implicitly_wait(10)
            user_name = []
            user_location = []
            for user in driver.find_elements_by_xpath("//*[@id='project-leads--leads-list']/div/div/div/div[2]"):
                user_name.append(user.find_element_by_xpath(".//a/span").text)
                user_location.append(user.find_element_by_xpath(".//span").text)
            self.datadict['Project'][i] = {'user_name' : user_name}
            self.datadict['Project'][i] = {'user_location' : user_location}
            project_description = driver.find_element_by_xpath("//*[@id='project-brief--brief-text']")
            self.datadict['Project'][i] = {'user_location' : project_description.text}
            if self.i == 0 :
                with open('data.json', 'w+') as js_file: 
                    json.dump(self.datadict['Project'], js_file)
            else:
                with open('data.json', 'a+') as js_file: 
                    json.dump(self.datadict['Project'], js_file)
            driver.back()
            driver.implicitly_wait(10)
            self.item['Project'] = self.datadict['Project']
        driver.close()


    def parse(self, response):
        resp = Selector(text=self.html)

        self.item['random'] = resp.xpath("/span").get()
        yield self.item