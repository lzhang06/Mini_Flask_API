
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
    def fetch_data(url):
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

        headers={'User-Agent':user_agent,}

        request=urllib.request.Request(url,None,headers) 
        response = urllib.request.urlopen(request)
        web_page = response.read()
        soups = BeautifulSoup(web_page)
        return soups

    fst_half_url = 'https://www.marinetraffic.com'
    weburl = 'https://www.marinetraffic.com/en/ais/index/search/all?keyword={}'.format(Keywords)
    soup = fetch_data(weburl)

    result_dict = collections.OrderedDict()
    count = 0
    i = 0
    while True:
        try:
            search_tab = soup.find('div', {'class': 'mt-table mt-table-responsive'})
            
            for row, link in zip(search_tab.findAll('tr'), search_tab.findAll('a', {'class': 'search_index_link'}, href=True)):
                col = row.findAll('td')
                if col:
                    vess_url = fst_half_url+link['href']

                    row = [i.text.strip() for i in col]
                    mmsi = re.search(r"mmsi:(.*)/", vess_url).group(1)
         
                        
                    result_dict[mmsi] = collections.OrderedDict()
                    result_dict[mmsi]['mmsi'] = mmsi
                    result_dict[mmsi]['Name'] = row[0]
                    result_dict[mmsi]['Result_Type'] = row[1]
                    result_dict[mmsi]['Description'] = row[2]
                    result_dict[mmsi]['Detail_Link'] = vess_url
                
    #             result_dict[mmsi]['details'] = bs4_vessel_detail(vess_url)
                
                print(count)
                count+=1
                
            next_button_ele = soup.find('span', {'class':'next'}).find('a', href=True)['href']
            
            go_next_link = fst_half_url+next_button_ele
            
            soup = fetch_data(go_next_link)
            print('go next')
        except Exception as e:
            print("found %s records"%len(result_dict))
            break


    
    return result_dict




test_value = 'shanghai'
if __name__ == '__main__':
    print(Scrap_Marine(test_value))







