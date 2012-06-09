import json
import cyclone.web

#from globaleaks.tip import tipHandler
#from globaleaks.receivers import groupsHandler, receiversHandler
#from globaleaks.stats import statsHandler
#from globaleaks.admin import adminHandler
from globaleaks.rest.handlers import *
from globaleaks.rest.utils import processChildren


class GLBackendAPI(cyclone.web.Application):
    def __init__(self):
        handlers = [(r'/', nodeHandler),
                    (r'/node', nodeHandler),
                    (r'/submission', submissionHandler),
                    (r'/submission/(.*)/submit_fields', submissionHandler,
                        dict(action="submit_fields")),
                    (r'/submission/(.*)/add_group', submissionHandler,
                        dict(action="add_group")),
                    (r'/submission/(.*)/finalize', submissionHandler,
                        dict(action="finalize")),
                    (r'/submission/(.*)/upload_file', submissionHandler,
                        dict(action="upload_file")),
                    (r'/tip/(.*)', tipHandler),
                    (r'/admin/receivers', adminReceiversHandler),
                    (r'/admin/config/node', nodeConfigHandler),
                    (r'/admin/config/delivery', deliveryConfigHandler),
                    (r'/admin/config/node', storageConfigHandler)]

        cyclone.web.Application.__init__(self, handlers, debug=True)
