import os 
import sys
from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

#import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient 

# TODO: use your own queues.
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://wzxeogxp:_BEoMhZ5z1Vlbgi7eTXm-OKkuR24dJj2@elephant.rmq.cloudamqp.com/wzxeogxp"
DEDUPE_NEWS_TASK_QUEUE_NAME = "dedupe-news-task-queue"
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://zoxnzdhf:VKEf6xNxQBpoTR7XXVWcpdJ87bsld1Kb@donkey.rmq.cloudamqp.com/zoxnzdhf"
SCRAPE_NEWS_TASK_QUEUE_NAME = "scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 10

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print('message is broken')
        return 
    
    task = msg
    text = None

    article = Article(task['url'])
    article.download()
    article.parse()
    #print(type(article.text))
    
    task['text'] = article.text.encode(encoding='UTF-8').decode(encoding='UTF-8')
    #print(type(task['text']))
    dedupe_news_queue_client.sendMessage(task)
    
while True:
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            # Parse and process the task
            try:
                handle_message(msg)
            except Exception as e:
                print(e)
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
