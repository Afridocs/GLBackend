import sys
import json

from twisted.python import log
from twisted.web import server, resource, http
from twisted.internet import reactor

import globaleaks
from globaleaks.rest import api

if __name__ == "__main__":
    log.startLogging(sys.stdout)
    interface = "127.0.0.1"
    port = 8082
    print "Starting GLBackend on %s:%s" % (interface, port)
    reactor.listenTCP(port, api.GLBackendAPI(), interface=interface)
    reactor.run()

