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
platforms = ['Windows 10', 'macOS 10.12', 'Linux']


def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        return end-start

    return wrapper


@timing
def call(driver, by, locator):
    driver.find_element(by, locator)

class getting_data():
    def get_ua(self, driver):
        return parse(driver.execute_script("return navigator.userAgent"))


    def post_es(self, locator, ua, stats, driver):
        es = Elasticsearch('http://es.lazycoder.io:80')
        index = 'browser-' + str(datetime.now().strftime("%Y-%m-%d-%H"))
        doc_type = "browser_locator"
        user_agent = self.to_dict(ua)
        body = {}
        body['user_agent'] = user_agent
        body["locator"] = locator
        body["exec_time"] = stats
        body["datetime"] = datetime.now()
        if str(type(driver)).__contains__("remote"):
            body["driver_type"]  = 'remote'
        else:
            body["driver_type"] = 'local'
        es.index(index, doc_type, body)


    def to_dict(self, ua):
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

    def run(self, d, by, locator):
        try:
            d.get('http://the-internet.herokuapp.com/large')
            bl = {}
            bl["By"] = by
            bl["Locator"] = locator
            stats = call(d, by, locator)
            ua = self.get_ua(d)
            self.post_es(bl, ua, stats, d)
            d.quit()
        except Exception as e:
            print(e)

