# -*- coding: utf-8 -*-
#
# jQuery File Upload Plugin cyclone example
# by Arturo Filastò <arturo@filasto.net>
#

from __future__ import with_statement

import json, re, urllib
import time, hashlib
import sys, os

from twisted.internet.defer import inlineCallbacks
from cyclone.web import RequestHandler, HTTPError, asynchronous

from globaleaks.utils import log
from globaleaks import models
from globaleaks import config

class FilesHandler(RequestHandler):
    filenamePrefix = "f_"
    # Set to None for no size restrictions
    maxFileSize = 500 * 1000 * 1000 # MB

    def acceptedFileType(self, type):
        regexp = None
        # regexp = re.compile('image/(gif|p?jpeg|(x-)?png)')
        if regexp and regexp.match(type):
            return True
        else:
            return False

    def validate(self, file):
        """
        Takes as input a file object and raises an exception if the file does
        not conform to the criteria.
        """
        if self.maxFileSize and file['size'] < self.maxFileSize:
            raise HTTPError(406, "File too big")

        if not self.acceptedFileType(file['type']):
            raise HTTPError(406, "File of unsupported type")

    def saveFile(self, data, filelocation):
        """
        XXX This is currently blocking. MUST be refactored to not be blocking
        otherwise we loose...
        """
        with open(filelocation, 'a+') as f:
            f.write(data)

    def process_file(self, file, submission_id, file_id):
        # XXX do here all the file sanitization stuff
        filename = re.sub(r'^.*\\', '', file['filename'])

        result = {}
        result['name'] = file_id
        result['type'] = file['content_type']
        result['size'] = len(file['body'])

        file_location = self.getFileLocation(submission_id, file_id)
        filetoken = submission_id

        result['token'] = filetoken

        log.debug("Saving file to %s" % file_location)
        self.saveFile(file['body'], file_location)
        return result

    def getFileLocation(self, submission_id, file_id):
        """
        Ovewrite me with your own function to generate the location of where
        the file should be stored.
        """
        if not os.path.isdir(config.advanced.submissions_dir):
            log.debug("%s does not exist. Creating it." % config.advanced.submissions_dir)
            os.mkdir(config.advanced.submissions_dir)

        this_submission_dir = os.path.join(config.advanced.submissions_dir, submission_id)

        if not os.path.isdir(this_submission_dir):
            log.debug("%s does not exist. Creating it." % this_submission_dir)
            os.mkdir(this_submission_dir)

        location = os.path.join(this_submission_dir, file_id)
        return location

    def options(self):
        pass

    def head(self):
        pass

    def get(self, *arg, **kw):
        pass

    @asynchronous
    @inlineCallbacks
    def post(self, submission_id):
        method_hack = self.get_arguments('_method')
        if method_hack and method_hack == 'DELETE':
            self.delete()

        results = []

        # XXX will this ever be bigger than 1?
        file_array, files = self.request.files.popitem()
        for file in files:
            start_time = time.time()

            submission = models.submission.Submission()
            file_id = yield submission.add_file(submission_id)
            log.debug("Created file with file id %s" % file_id)
            result = self.process_file(file, submission_id, file_id)
            result['elapsed_time'] = time.time() - start_time
            results.append(result)


        response = json.dumps(results, separators=(',',':'))

        if 'application/json' in self.request.headers.get('Accept'):
            self.set_header('Content-Type', 'application/json')
        self.write(response)
        self.finish()

    def delete(self):
        pass
