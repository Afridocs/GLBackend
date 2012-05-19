from twisted.web import resource

class receiversHandler(resource.Resource):
    def __init__(self, name="default"):
        resource.Resource.__init__(self)

    def render_GET(self, request):
        return "Receivers page."

    def render_POST(self, request):
        pass

class groupsHandler(resource.Resource):
    def __init__(self, name="default"):
        resource.Resource.__init__(self)

    def render_GET(self, request):
        return "groups page."

    def render_POST(self, request):
        pass


