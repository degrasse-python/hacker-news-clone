#! python3
import logging

from celery import group

from tasks import visit

def producer(users=100):
  """
  Create celery group of sig's for parallel processing

  Args:
      users - number of fake visits and clicks to generate.

  """

  # split board_data['data'] into chunks 
  ## -> call process step as on each chunk as a seperate subtask
  ### -> merge results
  group(visit.s() for i in range(users))().get()


### --- RUN --- ###
if __name__ == '__main__':
  producer()
  # run X visits
  logging.info("END RUN")