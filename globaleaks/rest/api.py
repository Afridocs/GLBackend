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

                    # Handlers for submission
                    (r'/submission', submissionHandler),
                    (r'/submission/(.*)', submissionHandler,
                        dict(action="submission_status")),
                    (r'/submission/(.*)/submit_fields', submissionHandler,
                        dict(action="submit_fields")),
                    (r'/submission/(.*)/add_group', submissionHandler,
                        dict(action="add_group")),
                    (r'/submission/(.*)/finalize', submissionHandler,
                        dict(action="finalize")),
                    (r'/submission/(.*)/upload_file', submissionHandler,
                        dict(action="upload_file")),

                    # Handler for Tip
                    (r'/tip/(.*)', tipHandler),

                    # Handler for receiver page
                    (r'/receiver/(.*)', receiverHandler),

                    # Handlers for Admin interface
                    (r'/admin/receivers', adminHandler,
                        dict(action="receivers")),
                    (r'/admin/notification', adminHandler,
                        dict(action="notification")),
                    (r'/admin/delivery', adminHandler,
                        dict(action="delivery")),
                    (r'/admin/storage', adminHandler,
                        dict(action="storage")),
                    (r'/admin/node', adminHandler,
                        dict(action="node"))]

        cyclone.web.Application.__init__(self, handlers, debug=True)
