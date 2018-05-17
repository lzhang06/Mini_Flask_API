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
import warnings
warnings.filterwarnings('ignore')


def bs4_vessel_detail(url):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

    headers={'User-Agent':user_agent,}
    
    request=urllib.request.Request(url,None,headers) 
    response = urllib.request.urlopen(request)
    web_page = response.read()

    soup = BeautifulSoup(web_page) 

    def match_class(target):
        def do_match(tag):
            classes = tag.get('class', [])
            return all(c in classes for c in target)
        return do_match

    ship_dict = collections.OrderedDict()
    ship_dict['General_Info'] = collections.OrderedDict()

    general_tab = soup.find('div', {'class': 'bg-info bg-light padding-10 radius-4 text-left'})
    for span, bullet in zip(general_tab.findAll('span'),general_tab.findAll('b')):
        span = ' '.join(span.text.strip()[:-1].split())
        b = bullet.text.strip()
        ship_dict['General_Info'][span] = b



    ship_dict['Geo_Info'] = collections.OrderedDict()
    geo_tab = soup.find('div', {'class': 'panel-body text-left short-line'})

    try:
        for each in geo_tab.findAll(match_class(['group-ib'])):
            for span, bullet in zip(each.findAll('span'),each.findAll('strong')):
                span = ' '.join(span.text.strip()[:-1].split())
                b = ' '.join(bullet.text.strip().split())
                ship_dict['Geo_Info'][span] = b

        if ship_dict['Geo_Info']['Position Received']:
            ship_dict['Geo_Info']['Position Received']= dparser.parse(ship_dict['Geo_Info']['Position Received'] ,fuzzy=True).strftime("%Y-%m-%d %H:%M")

        if ship_dict['Geo_Info']['Latitude / Longitude']:

            ship_dict['Geo_Info']['Latitude'],ship_dict['Geo_Info']['Longitude'] = [float(item.strip()[:-1]) for item in ship_dict['Geo_Info']['Latitude / Longitude'].split('/')]
#         del ship_dict['Geo_Info']['Latitude / Longitude']

    except Exception as e:
        print('No Records Found')


    #Clean Data
    if ship_dict['General_Info']['Length Overall x Breadth Extreme']:
        ship_dict['General_Info']['Length Overall'] = ship_dict['General_Info']['Length Overall x Breadth Extreme'].split('×')[0]
        ship_dict['General_Info']['Breadth Extreme'] = ship_dict['General_Info']['Length Overall x Breadth Extreme'].split('×')[1]
#         del ship_dict['Geo_Info']['Length Overall x Breadth Extreme']

    
    return ship_dict

if __name__ == '__main__':
    print(bs4_vessel_detail(r"https://www.marinetraffic.com/en/ais/details/ships/shipid:890932/mmsi:-8942151/vessel:QUEEN%20ELIZABETH%20I"))

