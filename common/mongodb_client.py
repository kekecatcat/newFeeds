from pymongo import MongoClient

MONGO_DB_HOST = "localhost"
MONGO_DB_PORT = 27017
DB_NAME = "news-feeds-server"

client = MongoClient("%s:%s" % (MONGO_DB_HOST, str(MONGO_DB_PORT)))

def get_db(db=DB_NAME):
    db = client[db]
    return db


