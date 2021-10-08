#! python3
from celery import Celery


REDIS_ENDPOINT = "redis-12568.c284.us-east1-2.gce.cloud.redislabs.com:12568"

app = Celery('proj',
          broker=REDIS_ENDPOINT,
          include=['hacker-news-clone.tasks'])

### --- RUN --- ###
if __name__ == '__main__':
  app.start()
