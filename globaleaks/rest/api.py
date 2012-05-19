import json
from twisted.web import resource

#from globaleaks.tip import tipHandler
#from globaleaks.receivers import groupsHandler, receiversHandler
#from globaleaks.stats import statsHandler
#from globaleaks.admin import adminHandler
from globaleaks.rest.handlers import *
from globaleaks.rest.utils import processChildren

class RESTful(resource.Resource):
    API = {'node': nodeHandler,
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
        resource.Resource.__init__(self)
        processChildren(self, self.API)

    def getChild(self, path, request):
        print path, request
        return resource.Resource()

if __name__ == "__main__":
    from twisted.internet import reactor
    from twisted.web import server
    reactor.listenTCP(8082, server.Site(RESTful()))
    reactor.run()
