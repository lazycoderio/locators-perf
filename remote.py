import random
import threading
from datetime import datetime
from functools import wraps
from threading import Thread
from time import time

import yaml
from selenium import webdriver
from elasticsearch import Elasticsearch
from selenium.webdriver.common.by import By
from user_agents import parse

from locator import getting_data

with open("config.yaml", 'r') as stream:
    config = yaml.load(stream)

browsers = ['firefox', 'chrome', 'safari', 'internet explorer', 'microsoftedge']
platforms = ['Windows 10', 'macOS 10.12', 'OS X 10.11', 'Linux']

def __main__():
    for _ in range(10000):

        desired_cap = {}
        desired_cap['browserName'] = random.choice(browsers)
        if desired_cap['browserName'] == 'microsoftedge' or desired_cap['browserName'] == 'internet explorer':
            #desired_cap['platform'] = 'Windows 10'
            pass
        elif desired_cap['browserName'] == 'safari':
            desired_cap['platform'] = 'macOS 10.12'
        else:
            desired_cap['platform'] = random.choice(platforms)
        desired_cap['name'] = 'Test - {}'.format(str(_))

        d = webdriver.Remote(
            command_executor='http://{}:{}@ondemand.saucelabs.com:80/wd/hub'.format(config['sauce']['user'],
                                                                                    config['sauce']['key']),
            desired_capabilities=desired_cap)

        l = getting_data()
        l.run(d, by = By.XPATH, locator = '//table[@id="large-table"]')
        l.run(d, by=By.PARTIAL_LINK_TEXT, locator='Elemental')
        l.run(d, by=By.LINK_TEXT, locator='Elemental Selenium')
        l.run(d, by=By.ID, locator='large-table')
        l.run(d, by=By.CSS_SELECTOR, locator='#large-table')
        l.run(d, by=By.CSS_SELECTOR, locator='.column-14')
        l.run(d, by=By.CLASS_NAME, locator='column-14')

if __name__ == '__main__':
    __main__()