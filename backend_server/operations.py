import json
import os
import pickle
import redis
import sys

from bson.json_util import dumps
from datetime import datetime

#import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_recommendation_service_client

from cloudAMQP_client import CloudAMQPClient

REDIS_HOST = "localhost"
REDIS_PORT = 6379

NEWS_TABLE_NAME = "news"
CLICK_LOGS_TABLE_NAME = "click_logs"

NEWS_LIMIT = 200
NEWS_LIST_BATCH_SIZE = 10
USER_NEWS_TIME_OOUT_IN_SECONDS = 60 # the time should be larger

LOG_CLICKS_TASK_QUEUE_URL = "amqp://ksnycjdm:i6SsuwItGSvKgudEbkYp7QdwNmuKjA7N@donkey.rmq.cloudamqp.com/ksnycjdm"
LOG_CLICKS_TASK_QUEUE_NAME = "log-clicks-task-queue"

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)


def getOneNews():
    db = mongodb_client.get_db()
    news = db[NEWS_TABLE_NAME].find_one()
    return news

def getNewsSummariesForUser(user_id, page_num):
    print("in operations.py, getNewsSummariesForUser")
    page_num = int(page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    # The final list of news to the returned.
    sliced_news = []
    if redis_client.get(user_id) is not None:
        news_digests = pickle.loads(redis_client.get(user_id))
        sliced_news_digests = news_digests[begin_index:end_index]
        # print (sliced_news_digests)
        db = mongodb_client.get_db()
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digests}}))
    else:
        print ("in else session")
        db = mongodb_client.get_db()
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        total_news_digests = list(map(lambda x: x['digest'], total_news))
        redis_client.set(user_id, pickle.dumps(total_news_digests))
        redis_client.expire(user_id, USER_NEWS_TIME_OOUT_IN_SECONDS)

        sliced_news = total_news[begin_index: end_index]

    # Get preference for the user.
    preference = news_recommendation_service_client.getPreferenceForUser(user_id)
    topPreference = None
    print (preference)

    if preference is not None and len(preference) > 0:
        topPreference = preference[0]

    for news in sliced_news:
        # Remove text field to save bandwidth
        del news['text']
        #if news['class'] == topPreference:
        #    news['reason'] = 'Recommend'
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'
    print 
        
    return json.loads(dumps(sliced_news))

def logNewsClickForUser(user_id, news_id):
    print("in operations.py, logNewsClickForUser func called")
    message = {'userId': user_id, 'newsId': news_id, 'timestamp':datetime.utcnow()}

    db = mongodb_client.get_db()
    db[CLICK_LOGS_TABLE_NAME].insert(message)

    # Send log task to machine learning service for prediction
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': str(datetime.utcnow())}
    cloudAMQP_client.sendMessage(message)