from twisted.web import resource

class tulipHandler(resource.Resource):
    def __init__(self, path):
        resource.Resource.__init__(self)
        self.path = path

    def render_GET(self, request):
        return "This is a tulip %s" % self.path


class tipHandler(resource.Resource):
    def __init__(self, name="default"):
        resource.Resource.__init__(self)

    def render_GET(self, request):
        return "Tips page.."

    def render_POST(self, request):
        pass

    def getChild(self, path, request):
        return tulipHandler(path)





