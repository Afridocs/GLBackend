import json
import sys
import os
import pickle
print __file__
# hack to add globaleaks to the sys path
cwd = '/'.join(__file__.split('/')[:-1])
sys.path.insert(0, os.path.join(cwd, '../../'))

from twisted.python import log
from twisted.trial import unittest
from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet.protocol import Protocol
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue

from storm.twisted.transact import Transactor
from storm.twisted.testing import FakeThreadPool, FakeTransactor
from storm.databases.sqlite import SQLite
from storm.uri import URI

from globaleaks import models
from globaleaks.db.tables import runCreateTable

from globaleaks.messages.dummy import requests

from globaleaks.db import tables

class BaseDBTest(unittest.TestCase):
    def setUp(self):
        self.threadpool = FakeThreadPool()
        self.transactor = Transactor(self.threadpool)
        self.database = SQLite(URI("sqlite:///test.db"))

    def mock_model(self, model=None):
        if model:
            mock = model()
        else:
            mock = self.baseModel()
        mock.transactor = self.transactor
        mock.database = self.database
        return mock

    @inlineCallbacks
    def create_table(self, model=None):
        if not model:
            model = self.baseModel
        try:
            yield runCreateTable(model, self.transactor, self.database)
        except:
            pass

class TablesTest(BaseDBTest):
    def disable_test_base(self):
        # XXX disabled because of WIP on database
        good_query = "CREATE TABLE submission (creation_time VARCHAR, fields BLOB, folder_gus INTEGER, id INTEGER, receivers BLOB, submission_gus VARCHAR, PRIMARY KEY (id))"
        self.assertEqual(tables.generateCreateQuery(models.submission.Submission),
                good_query)

    @inlineCallbacks
    def test_create(self):
        yield self.create_table(models.submission.Submission)

class TestSubmission(BaseDBTest):

    baseModel = models.submission.Submission
    submission_gus = u'r_testsubmissionid'

    @inlineCallbacks
    def test_create_table(self):
        yield self.create_table()

    @inlineCallbacks
    def create_dummy_submission(self, submission_gus):
        test_submission = self.mock_model()
        test_submission.submission_gus = submission_gus
        test_submission.folder_gus = 0

        test_submission.fields = requests.submissionStatusPost['fields']
        test_submission.context_selected = requests.submissionStatusPost['context_selected']
        yield test_submission.save()

    @inlineCallbacks
    def test_create_new_submission(self):
        submission = self.mock_model()
        res = yield submission.new()

    @inlineCallbacks
    def test_submission_status(self):
        yield self.create_table()

        test_submission = self.mock_model()
        my_gus = self.submission_gus+'stat'

        yield self.create_dummy_submission(my_gus)
        status = yield test_submission.status(my_gus)

        self.assertEqual(status['fields'],
                requests.submissionStatusPost['fields'])
        self.assertEqual(status['context_selected'],
                requests.submissionStatusPost['context_selected'])

    @inlineCallbacks
    def test_finalize_submission(self):
        yield self.create_table()

        test_submission = self.mock_model()
        my_gus = self.submission_gus+'fina'

        yield self.create_table(models.tip.InternalTip)
        yield self.create_table(models.tip.Tip)

        yield self.create_dummy_submission(my_gus)
        try:
            yield test_submission.complete_submission(my_gus, u'1234567890')
        except Exception, e:
            print e

class TestReceivers(BaseDBTest):
    baseModel = models.receiver.Receiver

    @inlineCallbacks
    def create_tables(self):
        yield self.create_table(models.receiver.Receiver)
        yield self.create_table(models.admin.ReceiverContext)
        yield self.create_table(models.admin.Context)

    @inlineCallbacks
    def test_create_tables(self):
        yield self.create_tables()

    @inlineCallbacks
    def test_create_dummy_receivers(self):
        yield self.create_tables()

        test_receiver = self.mock_model()

        initial_count = yield test_receiver.count()
        result = yield test_receiver.create_dummy_receivers()

        receiver_count = yield test_receiver.count()
        self.assertEqual(receiver_count, initial_count + 4)

    @inlineCallbacks
    def test_add_receiver_to_context(self):
        yield self.create_tables()

        context_gus = u'c_thisisatestcontext'
        test_receiver = self.mock_model()
        test_context = self.mock_model(models.admin.Context)
        test_context.name = u'test context'
        test_context.context_gus = context_gus

        yield test_context.save()

        result = yield test_receiver.create_dummy_receivers()

        receiver_gus = result[0]['receiver_gus']
        yield test_context.add_receiver(context_gus, receiver_gus)


class TestTip(BaseDBTest):
    pass


