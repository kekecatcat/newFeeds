from flask import Flask
from flask_jsonrpc import JSONRPC
import operator
import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"

SERVER_HOST = 'localhost'
SERVER_PORT = 5050

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/')


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


# Ref: https://www.python.org/dev/peps/pep-0485/#proposed-implementation
# Ref: http://stackoverflow.com/questions/5595425/what-is-the-best-way-to-compare-floats-for-almost-equality-in-python
@jsonrpc.method('getPreferenceForUser')
def getPreferenceForUser(user_id):
    print ("call getPreferenceForUser")
    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': user_id})
    print (model)
    if model is None:
        return []
    
    sorted_tuples = sorted(model['preference'].items(), key=operator.itemgetter(1), reverse=True)
    sorted_list = [x[0] for x in sorted_tuples]
    sorted_value_list = [x[1] for x in sorted_tuples]

    # If the first preference is same as the last one, the preference makes no sense
    if isclose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
        return []
    
    return sorted_list

print ("Starting HTTP server on %s:%d" % (SERVER_HOST, SERVER_PORT))
app.run(host=SERVER_HOST,port=SERVER_PORT,debug=True)
