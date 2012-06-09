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
    def setUp(self):
        self.port = reactor.listenTCP(31415, api.GLBackendAPI(), interface="127.0.0.1")
        if debug:
            log.startLogging(sys.stdout)
        self.addCleanup(self.port.stopListening)
        self.submission_id = ""

    def _do_submission_operation(self, data, operation, body=None,
            datafunction=None, responsefunction=None):
        url = 'http://127.0.0.1:31415/submission/'+str(self.submission_id)+'/'+str(operation)
        d = self.agent.request('POST',
                url,
                None, body)

        def cbFinished(data):
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

    def test_create_submission(self):
        d = self.agent.request('POST',
                'http://127.0.0.1:31415/submission', None, None)

        def cbFinished(data):
            parsed = json.loads(data)
            self.submission_id = parsed['submission_id']

        def cbResponse(response):
            finished = Deferred()
            response.deliverBody(BodyReceiver(finished))
            finished.addCallback(cbFinished)
            return finished

        d.addCallback(cbResponse)
        return d

    def test_add_fields(self):
        def rfunction(response):
            self.assertEqual(response.code, 202)

        d = self.test_create_submission()
        d.addCallback(self._do_submission_operation, "submit_fields",
                responsefunction=rfunction)
        return d

    def test_add_fields_to_invalid_submission(self):
        self.submission_id = "invalid"
        def rfunction(response):
            self.assertEqual(response.code, 204)
        def dfunction(data):
            parsed = json.load(data)
            self.assertEqual(parsed['error-message'], "submission ID is invalid")

        self._do_submission_operation(None, "submit_fields", datafunction=dfunction, responsefunction=rfunction)

