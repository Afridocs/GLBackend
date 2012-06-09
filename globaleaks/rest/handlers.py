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
           'adminHandler', 'tipHandler', 'receiverHandler']

class GLHandler(cyclone.web.RequestHandler):
    def generic_error(self):
        self.write({'error': 'generic'})

class nodeHandler(GLHandler):
    def get(self):
        self.write(config.node_info)

class submissionHandler(GLHandler):
    """
    Responsible for handling everything that goes under the /submission
    tree.
    """
    def initialize(self, action=None):
        self.action = action
        print action

    def _parse_request(self):
        try:
            request = json.loads(self.request.body)
        except:
            request = None
        return request

    def invalid_submission(self):
        self.set_status(204)
        r = {'error-code': 1, 'error-message': 'submission ID is invalid'}
        self.write(r)

    def get(self, submission_id=None):
        """
        Process GET requests:
            * /submission
            * /submission/<ID>
            * /submission/<ID>/upload_file
        """
        if submission_id:
            submission = submission_factory.submissions.get(submission_id)
            if submission is None:
                self.invalid_submission()
            else:
                process = getattr(self, "get_" + self.action)
                response = process(submission)
        else:
            self.set_status(501)

    def get_submission_status(self, submission):
        self.set_status(200)
        self.write(submission.get_status())

    def post(self, submission_id=None, other=None):
        """
        Process POST requests:
            * /submission
            * /submission/<ID>/submit_fields
            * /submission/<ID>/add_group
            * /submission/<ID>/finalize
            * /submission/<ID>/upload_file
        """
        response = ""
        if not submission_id:
            response = self.post_create_submission()
        elif self.action:
            submission = submission_factory.submissions.get(submission_id)
            if submission is None:
                self.invalid_submission()
            else:
                request = self._parse_request()
                process = getattr(self, "post_" + self.action)
                response = process(submission, request)

    def post_create_submission(self):
        """
        This creates an empty submission and returns the ID to be used when
        referencing it as a whistleblower. ID is a random string.
        """
        self.set_status(201)
        self.write(submission_factory.create())

    def post_submit_fields(self, submission, request):
        """
        does the submission of the fields that are supported by the node in
        question and update the selected submission_id (POST only)
        """
        submission.submit_fields(request)
        self.set_status(202)


    def post_add_group(self, submission, request):
        """
        adds a group to the list of recipients for the selected submission.
        group are addressed by their ID (POST only)
        """
        submission.add_group(request)
        self.set_status(202)

    def post_finalize(self, submission, request):
        """
        completes the submission in progress, give to the server the receipt
        secret and confirm the receipt (or answer with a part of them).
        settings dependent. (POST only)
        """
        submission.finalize(request)

    def post_upload_file(self, submission, request):
        """
        upload a file to the selected submission_id (PUT only)
        """
        submission.upload_file(request)

class adminHandler(GLHandler):
    def post(self):
        """
        Process these POST requests:
            * /admin/receivers/
            * /admin/notification/
            * /admin/delivery/
            * /admin/storage/
            * /admin/node/
        """
        pass

    def get(self):
        """
        Process GET requests:
            * /admin/receivers/
            * /admin/notification/
            * /admin/delivery/
            * /admin/storage/
            * /admin/node/
        """
        pass


class receiverHandler(GLHandler):
    def get(self):
        """
        Process this GET:
            * /receiver/<ID>/overview
        """
    def post(self):
        """
        Process this POST:
            * /receiver/<ID>/overview
        """

class tipHandler(GLHandler):
    def post(self):
        """
        Process the POST requests:
            * /tip/<ID>/add_comment
            * /tip/<ID>/finalize_update
            * /tip/<ID>/pertinence

        """
        pass
    def get(self):
        """
        Process the GET requests:
            * /tip/<ID>
            * /tip/<ID>/update_file
            * /tip/<ID>/download_material
        """
        pass
