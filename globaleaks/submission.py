"""
    Submission
    **********

    Implements a GlobaLeaks submission.
"""
import random
import string

from globaleaks.utils import random_string

class Submission:
    factory = None
    fields = None

    materialset = []
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
            id = random_string(self.id_len, 'a-z,A-Z,0-9')
            if self._exists(id):
                id = None
        self.id = id

    def _exists(self, id):
        """
        Check if a particular submission ID exists

        :id: The id to look for.
        """
        return False

    def add_material(self, material):
        """
        Adds the material to the specified submission id.

        :material: append the material to the material set
        """
        self.materialset.append(material)
        return True

    def submit_fields(self, fields):
        """
        Add the fields to the submission.

        :fields: a dict containing the submitted fields
        """
        self.fields = fields
        return True

    def add_group(self, group):
        """
        Adds the group to the list of groups.

        :group: the group to be appendend to the group array.
        """
        self.groups.append(group)
        return True

    def finalize(self):
        """
        Finalize the submission and create data inside of the database.
        """
        return True

class SubmissionFactory:
    submissions = {}
    def create(self):
        submission = Submission()
        submission.factory = self

        # This should *never* happen.
        if self.submissions.get(submission.id) is not None:
            print "We just generated a conflicting submission ID. Bad entropy?"
            submission = Submission()

        self.submissions[submission.id] = submission
        return {'submission_id': submission.id}

submission_factory = SubmissionFactory()

