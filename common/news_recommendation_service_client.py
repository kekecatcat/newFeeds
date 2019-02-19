from jsonrpcclient.requests import Request
from jsonrpcclient.clients.http_client import HTTPClient

URL = "http://localhost:5050/"

client = HTTPClient(URL)

def getPreferenceForUser(userId):
    preference = client.send(Request('getPreferenceForUser', user_id=userId))
    #print ("preference list: %s" % str(preference.data.result))
    return preference.data.result