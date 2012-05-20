from twisted.web import resource

def processChildren(res, api):
    """
    Recursion is beauty.
    """
    for i, a in enumerate(api.items()):
        path, handler = a
        #print i
        if isinstance(handler, dict):
            #print "Got the dict :("
            #print "Res: %s" % res
            #print "Path: %s" % path
            #print "Handler: %s" % handler
            new_res = resource.Resource()
            if hasattr(res, 'path'):
                new_res.path = res.path
            res.putChild(path, processChildren(new_res, handler))

        else:
            #print "Got the handler ;)"
            #print "Res: %s" % res
            #print "Path: %s" % path
            #print "Handler: %s" % handler
            res.putChild(path, handler())
            if (len(api) - 1) == i:
                return res

