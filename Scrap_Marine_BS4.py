
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

def Scrap_Marine(Keywords, *args, **kwargs):
    q_location = kwargs.get('location', None)
    search_type = kwargs.get('search_type', None)

    def fetch_data(url):
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

        headers={'User-Agent':user_agent,}

        request=urllib.request.Request(url,None,headers) 
        response = urllib.request.urlopen(request)
        web_page = response.read()
        soups = BeautifulSoup(web_page, "lxml")
        return soups

    fst_half_url = 'https://www.marinetraffic.com'

    select_dict = {'all': 'All',
                 'call sign': '9',
                 'ex name': '4',
                 'imo': '3',
                 'light': '10',
                 'mmsi': '7',
                 'photographer': '5',
                 'port': '2',
                 'station': '6',
                 'vessel': '1'}
   
    if search_type is None:
        weburl = 'https://www.marinetraffic.com/en/ais/index/search/all?keyword={}'.format(Keywords)
    else:
        search_type = search_type.lower()

        weburl = 'https://www.marinetraffic.com/en/ais/index/search/all/keyword:{}/search_type:{}'.format(Keywords, select_dict[search_type])
    print(weburl)
    soup = fetch_data(weburl)

    result_list = list()
    count = 0
    
    while True:
        try:
            search_tab = soup.find('div', {'class': 'mt-table mt-table-responsive'})
            
            for row, link in zip(search_tab.findAll('tr')[1:], search_tab.findAll('a', {'class': 'search_index_link'}, href=True)):
                col = row.findAll('td')
                
                if col:
                    vess_url = fst_half_url+link['href']

                    row = [i.text.strip() for i in col]

                    mmsi_search = re.search(r"mmsi:(.*?)/", vess_url)
                    if mmsi_search:
                        mmsi = mmsi_search.group(1)
                    else: 
                        mmsi = ''

                    ship_search = re.search(r"shipid:(.*?)/", vess_url)
                    if ship_search:
                        ship_id = ship_search.group(1)
                    else: 
                        ship_id = ''              
                   
                    description = row[2].lower()
                    if description.find('[') == -1:
                        location = ''
                    else:
                        location = description[description.find('[')+1 : description.find(']')].lower()
#                     s[s.find("(")+1:s.find(")")]
                    
                    result_type = row[1].lower()

                    if result_type == 'Exname':
                        exname = description[description.find('(')+1 : description.find(')')].lower()
                    else:
                        exname =''         
                    
                    if q_location is None or location == q_location:
                        result_dict = collections.OrderedDict()
                        result_dict['MMSI'] = mmsi
                        result_dict['Name'] = row[0].lower()
                        result_dict['Result_Type'] = result_type
                        result_dict['Description'] = description
                        result_dict['Detail_Link'] = vess_url
                        result_dict['Ship_id'] = ship_id
                        result_dict['Location'] = location
                        result_dict['Exname'] = exname

                        result_list.append(result_dict)
                
                print(count)
                count+=1
                
            next_button_ele = soup.find('span', {'class':'next'}).find('a', href=True)['href']
            
            go_next_link = fst_half_url+next_button_ele
            
            soup = fetch_data(go_next_link)
            print('go next')
        except Exception as e:
            print("found %s records"%len(result_list))
            break

    #filter results

    for s_item, key in zip([search_type, q_location],['Result_Type', 'Location']):
        if s_item is None: pass
        else:
            print(s_item,key)
            result_list = [x for x in result_list if x[key] == s_item.lower()]


    q_paras = [Keywords, q_location, search_type]
    data = collections.OrderedDict()
    data['Brief_Search'] = collections.OrderedDict()
    data['Brief_Search']['Num_Found'] = len(result_list)
    data['Brief_Search']['Query_Parms'] = [i for i in q_paras if i is not None]

    data['Data'] = result_list
    #filter result



    return data




test_value = 'nanjing'
if __name__ == '__main__':
    print(Scrap_Marine(test_value))







