"""Backend Service"""
import pyjsonrpc

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

class RequestHandler(pyjsonrpc.HttpRequestHandler):

    @pyjsonrpc.rpcmethod
    def add(self, num1, num2): # pylint: disable=no-self-use
        """Test method"""
        '''
        :type num1: int
        :type num2: int
        '''
        print ("Add is called with %d and %d." % (num1, num2))
        return num1 + num2
    @pyjsonrpc.rpcmethod
    def getOneNews(self): # pylint: disable=no-self-use
        """ Get one news. """
        print ("getOneNews is called." % (num1, num2))
        return operations.getOneNews()
    
    @pyjsonrpc.rpcmethod
    def getSummariesForUser(self, user_id, page_num): # pylint: disable=no-self-use
        """ Get news summaries for a user. """
        print ("getSummariesForUser is called with %s and %s" % (user_id, page_num))
        return operations.getSummariesForUser(user_id, page_num)



# Threading HTTP-Server
HTTP_SERVER = pyjsonrpc.ThreadingHttpServer(
    server_address=(SERVER_HOST, SERVER_PORT),
    RequestHandlerClass=RequestHandler
)

print ("Starting HTTP server on %s:%d" % (SERVER_HOST, SERVER_PORT))
HTTP_SERVER.serve_forever()
