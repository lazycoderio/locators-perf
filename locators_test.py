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

browsers = ['firefox', 'chrome', 'safari', ' internet explorer', 'microsoftedge']
platforms = ['Windows 10', 'macOS 10.12', 'OS X 10.11', 'Linux']
with open("config.yaml", 'r') as stream:
    config = yaml.load(stream)

def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        return end-start

    return wrapper

class test():
    def __init__(self, driver):
        self.driver = driver

    def setup(self, by, locator):
        self.by = by
        self.locator = locator

    @timing
    def call(self, by, locator):
        self.driver.find_element(by, locator)


def get_ua(driver):
    return parse(driver.execute_script("return navigator.userAgent"))

def post_es(locator, ua, stats):
    es = Elasticsearch('http://es.lazycoder.io:80')
    index = 'browser-' + str(datetime.now().strftime("%Y-%m-%d-%H"))
    doc_type = "browser_locator"

    user_agent = to_dict(ua)

    body = {}
    body['user_agent'] = user_agent
    body["locator"] = locator
    body["exec_time"] = stats
    body["datetime"] = datetime.now()

    es.index(index, doc_type, body)


def to_dict(ua):
    d = {}
    b = {}
    o={}

    d['family'] = ua.device.family
    d['brand'] = ua.device.brand
    d['model'] = ua.device.model

    b['family'] = ua.browser.family
    b['version'] = ua.browser.version_string

    o['family'] = ua.os.family
    o['version'] = ua.os.version_string

    compiled={}
    compiled['browser'] = b
    compiled['os'] = o
    compiled['device'] = d
    compiled['mobile'] = ua.is_mobile
    compiled['pc'] = ua.is_pc
    compiled['tablet'] = ua.is_tablet

    return compiled

def run(d):
    try:
        d = webdriver.Remote(
            command_executor='http://{}:{}@ondemand.saucelabs.com:80/wd/hub'.format(config['sauce']['user'],
                                                                                    config['sauce']['key']),
            desired_capabilities=d)
        d.get('http://the-internet.herokuapp.com/large')
        t = test(d)
        by = By.ID
        locator = 'large-table'
        bl = {}
        bl["By"] = by
        bl["Locator"] = locator
        stats = t.call(by, locator)
        ua = get_ua(d)
        d.quit()
        post_es(bl, ua, stats)
    except Exception as e:
        print(e)

def __main__():
    threads = []

    for _ in range(10000):
        if threading.active_count() < 10:
            desired_cap = {}
            desired_cap['browserName'] = random.choice(browsers)
            if desired_cap['browserName'] == 'microsoftedge' or desired_cap['browserName'] == 'internet explorer':
                desired_cap['platform'] = 'Windows 10'
            elif desired_cap['browserName'] == 'safari':
                desired_cap['platform'] = 'macOS 10.12'
            else:
                desired_cap['platform'] = random.choice(platforms)
            desired_cap['name'] = 'Test - {}'.format(str(_))


            run(desired_cap)
        else:
            _ -= 1


if __name__ == '__main__':
    __main__()