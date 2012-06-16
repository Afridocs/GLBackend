import json
import sys

from twisted.python import log
from twisted.trial import unittest
from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet.protocol import Protocol
from twisted.internet.defer import Deferred, inlineCallbacks

from globaleaks.db import create_tables, threadpool
from globaleaks.db import transactor, database
from globaleaks.db.models import *

class DBTestCase(unittest.TestCase):

    def _cleanup(self, aa):
        threadpool.stop()

    def SetUp(self):
        self.addCleanup(self._cleanup)

    @inlineCallbacks
    def test_add_tip(self):
        from datetime import datetime
        yield create_tables()
        tip = InternalTip()
        tip.fields = {'hello': 'world'}
        tip.comments = {'hello': 'world'}
        tip.pertinence = 0
        expiration_time = datetime.now()
        tip.expiration_time = expiration_time

        yield tip.store()

        def findtip(what):
            from storm.locals import Store
            store = Store(database)
            x = list(store.find(InternalTip, InternalTip.id == what))
            return x

        r_tip = yield transactor.run(findtip, tip.id)
        self.assertEqual(r_tip[0].fields['hello'], 'world')
        self.assertEqual(r_tip[0].comments['hello'], 'world')

