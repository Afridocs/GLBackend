import json
import sys

from twisted.python import log
from twisted.trial import unittest
from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet.protocol import Protocol
from twisted.internet.defer import Deferred

from globaleaks.rest import api

global debug
debug = False

class BodyReceiver(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.data = ""

    def dataReceived(self, bytes):
        self.data += bytes

    def connectionLost(self, reason):
        self.finished.callback(self.data)

class SubmissionClientEmulationTestCase(unittest.TestCase):
    agent = Agent(reactor)

    def _create_submission(self):
        d = self.agent.request('POST',
                'http://127.0.0.1:31415/submission', None, None)

        def cbFinished(data):
            parsed = json.loads(data)
            if not self.submission_id:
                self.submission_id = parsed['submission_id']

        def cbResponse(response):
            finished = Deferred()
            response.deliverBody(BodyReceiver(finished))
            finished.addCallback(cbFinished)
            return finished

        d.addCallback(cbResponse)
        return d

    def setUp(self):
        self.port = reactor.listenTCP(31415, api.GLBackendAPI(), interface="127.0.0.1")
        if debug:
            log.startLogging(sys.stdout)
        self.submission_id = None
        return self._create_submission()

    def tearDown(self):
        self.port.stopListening()

    def _do_operation(self, operation, method="POST", body=None,
                      datafunction=None, responsefunction=None):
        url = 'http://127.0.0.1:31415/' + operation
        d = self.agent.request(method, url, None, body)

        def cbFinished(arg, data):
            if datafunction:
                datafunction(data)
            return data

        def cbResponse(response):
            finished = Deferred()
            if responsefunction:
                responsefunction(response)
            response.deliverBody(BodyReceiver(finished))
            finished.addCallback(cbFinished)
            return finished

        d.addCallback(cbResponse)
        return d

    def test_submit_fields(self):
        def rfunction(response):
            self.assertEqual(response.code, 202)

        operation = 'submission/'+str(self.submission_id)+'/submit_fields'
        self._do_operation(operation, responsefunction=rfunction)

    def test_submit_fields_to_invalid_submission(self):
        def rfunction(response):
            self.assertEqual(response.code, 204)

        def dfunction(data):
            parsed = json.load(data)
            self.assertEqual(parsed['error-message'], "submission ID is invalid")
            return

        operation = 'submission/invalid/submit_fields'
        self._do_operation(operation, datafunction=dfunction, responsefunction=rfunction)

    def test_add_group(self):
        def rfunction(response):
            self.assertEqual(response.code, 202)

        operation = 'submission/'+str(self.submission_id)+'/add_group'
        self._do_operation(operation, responsefunction=rfunction)


    def test_upload_file(self):
        def rfunction(response):
            self.assertEqual(response.code, 202)

        def dfunction(data):
            parsed = json.load(data)
            a_keys = ['filename', 'comment', 'size', 'content-type']
            b_keys = parsed.keys()
            a_keys.sort()
            b_keys.sort()
            self.assertEqual(a_keys, b_keys)
            return

        operation = 'submission/'+str(self.submission_id)+'/upload_file'
        self._do_operation(operation, datafunction=dfunction, responsefunction=rfunction)


