"""
The class implemented here defines the basic objects, specified
in REST-spec
"""

import os # required in GlbFile
import json # required in ModuleAdminConfig and ModuleDataStruct

class GlbFile:
    """
   { filename: <string>, comment: <String>, size: <Int, in bytes>, content-type: <string> }
    """

    def __init__(self, newfile, completed=False):
        self.comment = ''
        self.filetype = ''
        self.finalized = completed
        self.filename = newfile

    def change_name(self, newname):
        """
        this method useful when a temporary location is used
        """
        self.filename = newname

    def get_size(self):
        if os.access(self.filename, os.R_OK):
            self.filestats = os.stat(self.filename)
            return (self.filestats.st_size, self.finalized)
        else:
            # TODO log system error handling
            print "error in accessing " + self.filename
            return (0, False)

    def set_comment(self, comment):
        self.comment = comment

    def finalize(self):
        self.finalized = True
        # TODO use Mime or Magic to extract content type
        self.filetype = 'type/TODO'

    def get_gl_desc(self):
        ret = dict()

        if self.finalized:
            ret.update(dict({ 'filename' : '(incomplete) ' + self.filename }))
            ret.update(dict({ 'content-type' : '[undetected]' }))
        else:
            ret.update(dict({ 'filename' : self.filename}))
            ret.update(dict({ 'content-type' : self.filetype}))

        self.get_size()
        ret.update(dict({ 'size' : self.filestat.st_size}))
        ret.update(dict({ 'comment' : self.comment}))

        return ret

"""
This class provide a support for the developer who wrote module for GLBackend
The module shall be splitted in two kinds:
    1) module with admin configuration and receiver configuration
    2) module with admin configuration only

    this class provide the I/O object to interact between REST, ORM and extension modules
"""
class ModuleConf:

    def __init__(self, infos):
        self.name = infos[0]
        self.description = infos[1]
        self.builddict = ({'module-name' : self.name, 'service-message' : self.description})

    def add_bool(self, name, description, default=None):
        self.builddict.update({ 'checkbox': name, 'desc': description, 'default' : default})

    def add_password(self, name, description, default=None):
        self.builddict.update({ 'password': name, 'desc': description, 'default' : default})

    def add_text(self, name, description, default=None):
        self.builddict.update({ 'text': name, 'desc': description, 'default' : default})

    def get_json(self):
        return json.dumps(self.builddict)

    def acquire(self, expected_struct, received_json_data):
        print 'expected ' + str(type(expected_struct))
        print 'received ' + str(type(received_json_data))




# TODO
# LocalDict
