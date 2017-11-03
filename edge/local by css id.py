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


def __main__():
    for _ in range(10000):
        d = webdriver.Edge()
        l = getting_data()
        l.run(d, by = By.CSS_SELECTOR, locator = '#large-table')


if __name__ == '__main__':
    __main__()