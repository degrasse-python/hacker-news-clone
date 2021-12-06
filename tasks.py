#! python3
from __future__ import absolute_import, unicode_literals
import os
import logging
import uuid

import environ
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent

import numpy as np
from celery import Celery
from celery import (chord, 
                    group)

### --- GLOBALS --- ###
logging.basicConfig(filename="hackernews_fakeclicks_heroku.log", level=logging.DEBUG)
SITE = "https://ancient-plains-41902.herokuapp.com/"
# mean, std dev
MU, SIGMA = 0.7, 0.1
REDIS_ENDPOINT = "redis-12568.c284.us-east1-2.gce.cloud.redislabs.com:12568"
env = environ.Env(DEBUG=(bool, False))
data = {'visits': 0,
        'ask_conversions': 0,
        'show_conversions': 0,}
CELERYOPTIONS = {
    # Some subset of options
    "show_task_id": False,
    "show_task_execution_time": False,
    "show_task_args": False,
    "show_task_kwargs": False,
    "show_task_exception_info": False,
    "show_task_return_value": False,
    "failures_only": True,
    "slack_request_timeout": 2,
    "flower_base_url": None,
}
###   -----   SETUP_APP   -----   ###
app = Celery('ABtesting', broker="amqps://ocrscsid:Ymv7weyajasNvHfIRXxUlyMc5yxc2L3_@hornet.rmq.cloudamqp.com/ocrscsid") # broker=env('RABBITMQ'))
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

def plot():

  import matplotlib.pyplot as plt
  count, bins, ignored = plt.hist(s, 30, density=True)
  plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
                  np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
            linewidth=2, color='r')
  plt.show()


def visit(site=SITE, click=True, link='ask'):

  options = Options()
  options.headless = True
  firefox_profile = webdriver.FirefoxProfile()
  firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
  driver = webdriver.Firefox(options=options, firefox_profile=firefox_profile)
  # open headless browser:
  driver.get(SITE)
  
  try:
    driver.find_element_by_id(link)
    if click:
      driver.find_element_by_id(link).click()
      driver.quit()
  except:
    driver.quit()
  print("visits: %s ask conversions: %s show_conversions: %s" % (data['visits'], data['ask_conversions'], data['show_conversions']))

@app.task
def group_process_bid(chunk):
    """
    Create celery group of sig's for parallel processing

    Args:
        Chunks: (list) - list of chunks to process in parallel. 

    Returns:
        celery group of of data chunks to process using the get_board_id in parallel. 

    """

    return group([get_board_id.s(chunk[i]) for i in range(len(chunk))])


@app.task
def group_transform(board, board_info):
    return group([transform.s(board[0][i], board_info[i]) for i in range(len(board_info))])


def build_pipeline(**kwargs):
    pipeline = setup_chunk(kwargs['chunkd_nested_dict']) | map(process_step)
    pipeline.apply_async(args=[kwargs['api_url'], HEADER]) 

@app.task
def visit(site=SITE, data=data):
  ua = UserAgent()
  a = ua.random
  user_agent = ua.random
  options = Options()
  options.headless = True
  firefox_profile = webdriver.FirefoxProfile(set_proxy='20.94.229.106')
  firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
  uuid = uuid.uuid4()
  # We set the coordinate of where we want to be.
  firefox_profile.set_preference("geo.wifi.uri", 'data:application/json,{"location": {"lat": 38.912650, "lng":-77.036185}, "accuracy": 20.0}')
  # This line is necessary to avoid to prompt for geolocation authorization.
  firefox_profile.set_preference("geo.prompt.testing", True)
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
      driver.quit()
    else:
      driver.quit()
  except:
    sample_show = np.random.uniform(0, 1)
    if sample_show > 0.5:
      driver.quit()
    else:
      driver.find_element_by_id('show').click()
      data['show_conversions'] += 1 
      driver.quit()

  print("visits: %s ask conversions: %s show_conversions: %s" % (data['visits'], data['ask_conversions'], data['show_conversions']))


def fakeclick(users=10000, data=data):

  for i in range(0, users):
    print("Iteration %s /n visits: %s ask conversions: %s show_conversions: %s" % (i, data['visits'], data['ask_conversions'], data['show_conversions']))
    data['visits'] += 1
    sample_ask = np.random.normal(MU, SIGMA)
    if sample_ask > 0.5:
      visit()
      data['ask_conversions'] += 1 
    else:
      sample_show = np.random.uniform(0, 1)
      if sample_show > 0.5:
        visit(click=False, link='show')
      else:
        visit(click=True, link='show')
        data['show_conversions'] += 1


def sample(mu, sigma):
  return np.random.normal(MU, SIGMA)


### --- RUN --- ###
if __name__ == '__main__':
  app.start()
