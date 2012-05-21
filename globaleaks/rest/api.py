import json
from twisted.web import resource

#from globaleaks.tip import tipHandler
#from globaleaks.receivers import groupsHandler, receiversHandler
#from globaleaks.stats import statsHandler
#from globaleaks.admin import adminHandler
from globaleaks.rest.handlers import *
from globaleaks.rest.utils import processChildren

class RESTful(resource.Resource):
    API = {
       'info': nodeHandler,
       'submission': submissionHandler,
       'tip': tipHandler,
       'admin': {'receivers': adminReceiversHandler,
                 'config':  {'node': nodeConfigHandler,
                             'delivery': deliveryConfigHandler,
                             'storage': storageConfigHandler
                            }
                }
    }

    def __init__(self):
        """
        Create the root of the restful interface and create the children
        handlers for handlers that don't take a parameter.
        """
        resource.Resource.__init__(self)
        processChildren(self, self.API)

    def getChild(self, path, request):
        """
        When trying to access a child that does not exist return an empty
        resource.
        """
        print path, request
        return resource.Resource()

if __name__ == "__main__":
    from twisted.internet import reactor
    from twisted.web import server
    reactor.listenTCP(8082, server.Site(RESTful()))
    reactor.run()
