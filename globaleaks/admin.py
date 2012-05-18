from twisted.web import resource

class adminHandler(resource.Resource):
    def __init__(self, name="default"):
        resource.Resource.__init__(self)

    def render_GET(self, request):
        return "Admin page..."

    def render_POST(self, request):
        pass


