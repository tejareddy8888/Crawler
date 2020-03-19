#%%
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from scrapy.selector import Selector

#%%
fopt = Options()
fopt.headless=False
driver = webdriver.Firefox(executable_path="C:\\seleniumDrivers\\geckodriver.exe",options=fopt)
driver.get("https://launchforth.io/")

driver.implicitly_wait(5)

project_btn = driver.find_element_by_xpath("//span[@class='label' and contains(text(),'Projects')]")
project_btn.click()

driver.implicitly_wait(5)

category = 'Human Machine Interface'

category_btn = driver.find_element_by_xpath("//a[@class='ui suibutton' and contains(text(),'"+category+"')]")
category_btn.click()

driver.implicitly_wait(2)

print(driver.find_element_by_class_name("page-header__title").text)
#print(driver.page_source)

self_html = driver.page_source
i=0
for resp in driver.find_elements_by_xpath("//*[@class='grid__content__item']/div/h2"):
    i=i+1
for i in range(1,3):
    project_element = driver.find_element_by_xpath("//*[@class='grid__content__item']["+str(i)+"]")
    project_element.click()
    driver.implicitly_wait(10)
    for user in driver.find_elements_by_xpath("//*[@id='project-leads--leads-list']/div/div/div/div[2]"):
        user_name     = user.find_element_by_xpath(".//a/span").text
        user_location = user.find_element_by_xpath(".//span").text
        print(user_name,user_location)
    driver.back()
    driver.implicitly_wait(10)
driver.close()
#%%




