
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re
from bs4 import BeautifulSoup
import urllib
import collections
import dateutil.parser as dparser
import json
import sys, traceback
from vessel_detail import bs4_vessel_detail 

def Scrap_Marine(Keywords):
    path_chrome = '/Users/renyuzhang/Desktop/marine_api/chromedriver' 
    driver = webdriver.Chrome(path_chrome)
    driver.wait = WebDriverWait(driver, 10)

    driver.get("http://www.marinetraffic.com")

    delay = 3 # seconds

    try:
        
        
        path_input_bar = '//*[@id="mt_navbar_collapse"]/div/div[2]/div/div[1]/div/div/input'
        time.sleep(3)
        key_input = driver.find_element_by_xpath(path_input_bar)
        key_input.click()

        actions = ActionChains(driver)
        actions.send_keys(Keywords)
        actions.send_keys(Keys.ENTER)
        actions.perform()

        print('Search Sucessful')

    except NoSuchElementException:
        print('Seach Input elements not found')


    result_dict = collections.OrderedDict()
    count = 0
    while True:
        try:

            for each in driver.find_elements_by_class_name('search_index_link'):
                vess_url = each.get_attribute("href")
                vessel_name = each.get_attribute("text").strip()
                mmsi = re.search(r"mmsi:(.*)/", vess_url).group(1)            
                
                result_dict[mmsi] = collections.OrderedDict()

                
                result_dict[mmsi]["vessel_detail"] = bs4_vessel_detail(vess_url)
                result_dict[mmsi]["vessel_name"] = vessel_name
             
                print(count)
                count+=1
            next_button_path = '/html/body/main/div/div/div[1]/div[5]/div[2]/div[2]/div/div[2]/div/div[2]/span[4]/a'

            go_next_link = driver.find_element_by_xpath(next_button_path).get_attribute("href")
            
            driver.get(go_next_link)
            print('go next')
        except Exception as e:
            print("found %s records"%len(result_dict))
            break
    driver.quit()
    
    return result_dict




if __name__ == '__main__':
    print(Scrap_Marine(test_value))







