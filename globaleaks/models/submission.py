from twisted.internet.defer import returnValue
from storm.twisted.transact import transact
from storm.locals import *

from globaleaks.utils import idops, gltime
from globaleaks.models.base import TXModel
from globaleaks.models.tip import Folder, InternalTip, Tip

__all__ = ['Submission']

"""
This ORM implementation is called whistleblower, because contain the information mostly useful
for the WBs, other elements used by WBs stay on globaleaks.db.tips.SpecialTip
"""

class SubmissionError(Exception):
    pass

class Submission(TXModel):
    """
    This represents a temporary submission. Submissions should be stored here
    until they are transformed into a Tip.
    """
    __storm_table__ = 'submission'

    id = Int(primary=True)
    submission_id = Unicode() # Int()
    folder_id = Int()
    fields = Pickle()

    context_selected = Pickle()

    creation_time = Date()

    @transact
    def new(self):
        store = self.getStore()

        submission_id = idops.random_submission_id(False)
        creation_time = gltime.utcDateNow()
        response = {"submission_id": submission_id,
                    "creation_time": gltime.dateToTime(creation_time)}

        submission = Submission()
        submission.submission_id = submission_id
        submission.folder_id = 0
        submission.creation_time = creation_time

        store.add(submission)
        store.commit()
        store.close()
        return response

    @transact
    def update_fields(self, submission_id, fields):
        store = self.getStore()
        s = store.find(Submission, Submission.submission_id==submission_id).one()

        if not s.fields:
            s.fields = {}

        for k, v in fields.items():
            s.fields[k] = v

        store.commit()
        store.close()


    @transact
    def select_context(self, submission_id, context):
        store = self.getStore()
        s = store.find(Submission, Submission.submission_id==submission_id).one()
        s.context_selected = context
        store.commit()
        store.close()

    @transact
    def status(self, submission_id):
        store = self.getStore()
        s = store.find(Submission, Submission.submission_id==submission_id).one()

        status = {'context_selected': s.context_selected,
                  'fields': s.fields}

        store.commit()
        store.close()
        return status

    @transact
    def create_tips(self, submission_id, receipt):
        store = self.getStore()
        try:
            s = store.find(Submission,
                Submission.submission_id==submission_id).one()
        except Exception, e:
            store.commit()
            store.close()
            raise Exception("Collision detected! HELP THE WORLD WILL END!")

        if not s:
            store.commit()
            store.close()
            raise Exception("Did not find a submission with that ID")

        internal_tip = InternalTip()
        internal_tip.fields = s.fields
        store.add(internal_tip)

        whistleblower_tip = Tip()
        whistleblower_tip.internal_tip_id = internal_tip.id
        whistleblower_tip.address = receipt
        store.add(whistleblower_tip)

        if not s.context_selected:
            store.commit()
            store.close()
            raise SubmissionError("No receivers selected")

        # XXX lookup the list of receivers and create their tips too.
        # receivers = Context.get_receivers(s.context_selected)


        # Delete the temporary submission
        store.remove(s)

        store.commit()
        store.close()

