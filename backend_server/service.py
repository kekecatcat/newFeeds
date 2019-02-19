"""Backend Service"""
from flask import Flask
from flask_jsonrpc import JSONRPC

import operations

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/')

# @jsonrpc.method('index')
# def index():
#     return u'Welcome to Flask JSON-RPC'

@jsonrpc.method('add')
def add(num1, num2): # pylint: disable=no-self-use
    """Test method"""
    '''
    :type num1: int
    :type num2: int
    '''
    print ("Add is called with %d and %d." % (num1, num2))
    return num1 + num2

@jsonrpc.method('getOneNews')
def getOneNews(): # pylint: disable=no-self-use
    """ Get one news. """
    print ("getOneNews is called." % (num1, num2))
    return operations.getOneNews()

@jsonrpc.method('getNewsSummariesForUser')
def getNewsSummariesForUser(user_id, page_num): # pylint: disable=no-self-use
    """ Get news summaries for a user. """
    print ("getSummariesForUser is called with %s and %s" % (user_id, page_num))
    return operations.getNewsSummariesForUser(user_id, page_num)

@jsonrpc.method('logNewsClickForUser')
def logNewsClickForUser(user_id, news_id): #pylint: disable=no-self-use
    """ Log news click for user. """
    print ("logNewsClickForUser is called with %s and %s" % (user_id, news_id))
    return operations.logNewsClickForUser(user_id, news_id)

app.run(host=SERVER_HOST,port=SERVER_PORT,debug=True)

