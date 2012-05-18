import json
from twisted.web import resource

from globaleaks.tip import tipHandler
from globaleaks.targets import groupsHandler, targetsHandler
from globaleaks.stats import statsHandler
from globaleaks.admin import adminHandler

class infoHandler(resource.Resource):
    def __init__(self, name="default"):
        self.name = name
        resource.Resource.__init__(self)

    def render_GET(self, request):
        return json.dumps(API.keys())

    def render_POST(self, request):
        pass

API = {'info': infoHandler,
       'tip': tipHandler,
       'targets': targetsHandler,
       'groups': groupsHandler,
       'admin': adminHandler,
       'stats': statsHandler}

class EmptyChild(resource.Resource):
    def __init__(self, name="default"):
        self.name = name
        resource.Resource.__init__(self)

    def render_GET(self, request):
        return str(self.name)

    def render_POST(self, request):
        return str(self.name)

    def getChild(self, path, request):
        print "In child..."
        print self, path
        return EmptyChild(path)


class RESTful(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)
        for k, v in API.items():
            self.putChild(k, v(k))

    def getChild(self, path, request):
        print path, request
        return EmptyChild()

