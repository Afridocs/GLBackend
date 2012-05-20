"""
    Submission
    **********

    Implements a GlobaLeaks submission.
"""
import random
import string

from globaleaks.utils import random_string

materialset = []
fields = None
groups = []
id_len = 100
def __init__(self, id = None):
    """
    Create a new submission and return it's submission ID or instantiate a
    submission object with the specified id.

    :id: if set to not None instantiate the submission object with the
         specified id.
    """
    if id and self._exists(id):
        return id

    while not id:
        id = random_string(id_len, 'a-z,A-Z,0-9')
        if self._exists(id):
            id = None
    self.id = id
    return id

def _exists(self, id):
    """
    Check if a particular submission ID exists

    :id: The id to look for.
    """
    return False

def add_material(self, id, material):
    """
    Adds the material to the specified submission id.
    """
    if not self._exists(id):
        return False
    self.materialset.append(material)
    return True

def submit_fields(self, id, fields):
    if not self._exists(id):
        return False
    self.fields = fields
    return True

def add_group(self, id, group):
    if not self._exists(id):
        return False
    self.groups.append(group)
    return True

def finalize(self, id):
    if not self._exists(id):
        return False
    return True

