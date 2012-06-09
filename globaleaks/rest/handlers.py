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

class GLHandler(cyclone.web.RequestHandler):
    def generic_error(self):
        self.write({'error': 'generic'})

class nodeHandler(GLHandler):
    def get(self):
        self.write(config.node_info)

class submissionHandler(GLHandler):
    def initialize(self, action=None):
        self.action = action
        print action

    def invalid_submission(self):
        self.set_status(204)
        r = {'error-code': 1, 'error-message': 'submission ID is invalid'}
        self.write(r)

    def create_submission(self):
        """
        This creates an empty submission and returns the ID to be used when
        referencing it as a whistleblower. ID is a random string.
        """
        self.write(submission_factory.create())

    def submit_fields(self, submission):
        """
        does the submission of the fields that are supported by the node in
        question and update the selected submission_id (POST only)
        """
        data = self.get_argument("body", None)
        submission.submit_fields(data)
        self.set_status(202)


    def add_group(self, submission):
        """
        adds a group to the list of recipients for the selected submission.
        group are addressed by their ID (POST only)
        """

    def finalize(self, submission):
        """
        completes the submission in progress, give to the server the receipt
        secret and confirm the receipt (or answer with a part of them).
        settings dependent. (POST only)
        """
        pass

    def upload_file(self, submission):
        """
        upload a file to the selected submission_id (PUT only)
        """

    def post(self, submission_id=None, other=None):
        response = ""
        if not submission_id:
            response = self.create_submission()
        elif self.action:
            submission = submission_factory.submissions.get(submission_id)
            if submission is None:
                self.invalid_submission()
            else:
                process = getattr(self, self.action)
                response = process(submission)

    def get(self, submission_id=None):
        self.write(str(self.__class__))

class adminReceiversHandler(GLHandler):
    def get(self, request):
        self.write(str(self.__class__))

class nodeConfigHandler(GLHandler):
    def get(self, request):
        self.write(str(self.__class__))

class deliveryConfigHandler(GLHandler):
    def get(self, request):
        self.write(str(self.__class__))

class storageConfigHandler(GLHandler):
    def get(self, request):
        self.write(str(self.__class__))

# Tip Handlers

class addCommentHandler(GLHandler):
    def get(self, request, parameter):
        self.write(str(self.__class__) + "<br>" + parameter)

class pertinenceHandler(GLHandler):
    def get(self):
        self.write(str(self.__class__) + "<br>" + parameter)

class downloadMaterialHandler(GLHandler):
    def get(self, request, parameter):
        self.write(str(self.__class__) + "<br>" + parameter)

class addDescriptionHandler(GLHandler):
    def get(self, request, parameter):
        self.write(str(self.__class__))

tipAPI = {'download_material': downloadMaterialHandler,
          'add_comment': addCommentHandler,
          'pertinence': pertinenceHandler,
          'add_description': addDescriptionHandler}


class tipHandler(GLHandler):
    def get(self):
        self.write("tip")



