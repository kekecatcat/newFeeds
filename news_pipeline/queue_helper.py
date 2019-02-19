import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import news_api_client
from cloudAMQP_client import CloudAMQPClient

# ToDO: use your own queue.
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://zoxnzdhf:VKEf6xNxQBpoTR7XXVWcpdJ87bsld1Kb@donkey.rmq.cloudamqp.com/zoxnzdhf"
SCRAPE_NEWS_TASK_QUEUE_NAME = "scrape-news-task-queue"
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://wzxeogxp:_BEoMhZ5z1Vlbgi7eTXm-OKkuR24dJj2@elephant.rmq.cloudamqp.com/wzxeogxp"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"

def clearQueue(queue_url, queue_name):
    scrape_news_queue_client = CloudAMQPClient(queue_url, queue_name)

    num_of_messages = 0

    while True:
        if scrape_news_queue_client is not None:
            msg = scrape_news_queue_client.getMessage()
            if msg is None:
                print ("Cleared %d messages." % num_of_messages)
                return
            num_of_messages += 1

if __name__ == "__main__":
    clearQueue(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
    clearQueue(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
