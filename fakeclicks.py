import logging

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import numpy as np

# setup logging
logging.basicConfig(filename="hackernews_fakeclicks_heroku", level=logging.DEBUG)

SITE = "https://ancient-plains-41902.herokuapp.com/"
# mean, std dev
MU, SIGMA = 0.7, 0.1

data = {'visits': 0,
        'ask_conversions': 0,
        'show_conversions': 0,}

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
  driver = webdriver.Firefox(options=options)
  print("Headless Firefox Initialized")
  # open headless browser:
  driver.get("https://ancient-plains-41902.herokuapp.com/")
  
  if driver.find_element_by_id(link):
    if click:
      driver.find_element_by_id(link).click()
      driver.quit()
  else:
    driver.quit()
  # print("Visit")

def sample(mu, sigma):
  return np.random.normal(MU, SIGMA)

# run X visits
for i in 10e6:
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


logging.info("visits: %s ask conversions: %s show_conversions: %s" % (data['visits'], data['ask_conversions'], data['show_conversions']))