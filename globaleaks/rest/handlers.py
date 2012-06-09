"""
    Handler
    *******

    This contains all of the handlers for the REST interface.
    Should not contain any logic that is specific to the operations to be done
    by the particular REST interface.
"""
import json
import cyclone.web
from twisted.web import resource
from globaleaks.config import config
from globaleaks.submission import submission_factory

__all__ = ['nodeHandler','submissionHandler',
           'adminReceiversHandler', 'nodeConfigHandler',
           'deliveryConfigHandler', 'storageConfigHandler',
           'addCommentHandler', 'pertinenceHandler',
           'downloadMaterialHandler', 'addDescriptionHandler', 'tipHandler']

class nodeHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write(config.node_info)

class submissionHandler(cyclone.web.RequestHandler):
    def post(self, submission_id=None):
        if not submission_id:
            response = submission_factory.create()
            self.write(response)

    def get(self, submission_id=None):
        self.write(str(self.__class__))

class adminReceiversHandler(cyclone.web.RequestHandler):
    def get(self, request):
        self.write(str(self.__class__))

class nodeConfigHandler(cyclone.web.RequestHandler):
    def get(self, request):
        self.write(str(self.__class__))

class deliveryConfigHandler(cyclone.web.RequestHandler):
    def get(self, request):
        self.write(str(self.__class__))

class storageConfigHandler(cyclone.web.RequestHandler):
    def get(self, request):
        self.write(str(self.__class__))

# Tip Handlers

class addCommentHandler(cyclone.web.RequestHandler):
    def get(self, request, parameter):
        self.write(str(self.__class__) + "<br>" + parameter)

class pertinenceHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write(str(self.__class__) + "<br>" + parameter)

class downloadMaterialHandler(cyclone.web.RequestHandler):
    def get(self, request, parameter):
        self.write(str(self.__class__) + "<br>" + parameter)

class addDescriptionHandler(cyclone.web.RequestHandler):
    def get(self, request, parameter):
        self.write(str(self.__class__))

tipAPI = {'download_material': downloadMaterialHandler,
          'add_comment': addCommentHandler,
          'pertinence': pertinenceHandler,
          'add_description': addDescriptionHandler}


class tipHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write("tip")



