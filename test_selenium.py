import os
import logging
import uuid
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent

import numpy as np


SITE = "https://ancient-plains-41902.herokuapp.com/"
# mean, std dev
MU, SIGMA = 0.7, 0.1
GEOLOCATION_PATH = "./geo.json"

data = {'visits': 0,
        'ask_conversions': 0,
        'show_conversions': 0,}


ua = UserAgent()
a = ua.random
user_agent = ua.random
options = Options()
# options.headless = True
options.add_argument('--lang=en_US')
options.add_argument("--enable-javascript")
firefox_profile = webdriver.FirefoxProfile()

firefox_profile.set_preference("javascript.enabled", True)
uuid = uuid.uuid4()
# We set the coordinate of where we want to be.
# This line is necessary to avoid to prompt for geolocation authorization.
firefox_profile.set_preference("geo.prompt.testing.allow", True)
firefox_profile.set_preference('geo.wifi.uri', GEOLOCATION_PATH)

driver = webdriver.Firefox(options=options, firefox_profile=firefox_profile)
# open headless browser:
driver.get(SITE)
data['visits'] += 1
try:
  driver.find_element_by_id('ask')
  sample_ask = np.random.normal(MU, SIGMA)
  if sample_ask > 0.5:
    #conversion
    driver.find_element_by_id("ask").click()
    data['ask_conversions'] += 1 
    time.sleep(5)
    driver.quit()
  else:
    driver.quit()
except:
  sample_show = np.random.uniform(0, 1)
  if sample_show > 0.5:
    driver.quit()
  else:
    #conversion
    driver.find_element_by_id('show').click()
    time.sleep(5)
    data['show_conversions'] += 1 
    driver.quit()

print("visits: %s ask conversions: %s show_conversions: %s" % (data['visits'], data['ask_conversions'], data['show_conversions']))
