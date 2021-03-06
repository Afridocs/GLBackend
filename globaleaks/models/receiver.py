# -*- coding: UTF-8
#
#   models/receiver
#   ***************
# 
# Storm DB implementation of the receiver table and ORM

from storm.exceptions import NotOneError
from storm.twisted.transact import transact
from storm.locals import Int, Pickle, Date, Unicode, Bool

from globaleaks.models.context import Context
from globaleaks.models.base import TXModel
from globaleaks.utils import log, idops, gltime
from globaleaks.rest.errors import ContextGusNotFound, ReceiverGusNotFound, InvalidInputFormat

__all__ = ['Receiver']

# The association between Receiver and Context is performed in models/admin.py ContextReceivers table

class Receiver(TXModel):
    """
    Receiver description model, some Receiver dependent information are
    also in globaleaks.models.plugin ReceiverConfs table
    """
    __storm_table__ = 'receivers'

    receiver_gus = Unicode(primary=True)

    creation_date = Date()
    update_date = Date()
    last_access = Date()

    # Those four variable can be changed by the Receiver
    name = Unicode()
    description = Unicode()
    # Tags and know_languages reflect in the Context
    tags = Pickle()
    know_languages = Pickle()

    # Those four would be removed and used ReceiverConfs.receiver_gus
    # reference, fields, profile, etc
    notification_selected = Unicode()
    delivery_selected = Unicode()
    notification_fields = Pickle()
    delivery_fields = Pickle()

    # Admin choosen options
    can_delete_submission = Bool()
    can_postpone_expiration = Bool()
    can_configure_delivery = Bool()
    can_configure_notification = Bool()
    admin_description = Unicode() # XXX: update API, scripts and outputs

    # receiver_tier = 1 or 2. Mean being part of the first or second level
    # of receivers body. if threshold is configured in the context. default 1
    receiver_level = Int()

    # this for keeping the same feature of GL 0.1
    secret = Unicode()

    # list of context_gus which receiver is associated
    contexts = Pickle()

    @transact
    def count(self):
        store = self.getStore('receiver count')
        receiver_count = store.find(Receiver).count()
        store.commit()
        store.close()
        return receiver_count

    @transact
    def new(self, receiver_dict):
        """
        @receiver_dict: here is supposed to be already sanitized
        @return: the receiver_gus or raise an exception

        Behold! this method convert a soulless dict in Tha Man, The Choosen
        One that want review the whistles blowed documents. It's a sort of
        transparency baptism: here you get your GlobaLeaks Unique String, sir!
        """

        store = self.getStore('receiver new')

        baptized_receiver = Receiver()

        try:
            baptized_receiver._import_dict(receiver_dict)
        except KeyError:
            store.close()
            raise InvalidInputFormat("Error near the Storm")

        baptized_receiver.receiver_gus = idops.random_receiver_gus()
        baptized_receiver.contexts = []

        baptized_receiver.creation_date = gltime.utcDateNow()
        baptized_receiver.update_date = gltime.utcDateNow()
        # last_access is not initialized

        store.add(baptized_receiver)
        store.commit()
        store.close()

        return baptized_receiver.receiver_gus


    @transact
    def admin_update(self, receiver_gus, receiver_dict):
        """
        This is the method called by the admin for change receiver preferences.
        may edit more elements than the next method (self_update)
        the dict need to be already validated
        """

        store = self.getStore('receiver admin_update')

        # I didn't understand why, but NotOneError is not raised even if the search return None
        try:
            requested_r = store.find(Receiver, Receiver.receiver_gus == unicode(receiver_gus)).one()
        except NotOneError:
            store.close()
            raise ReceiverGusNotFound
        if requested_r is None:
            store.close()
            raise ReceiverGusNotFound

        try:
            requested_r._import_dict(receiver_dict)
        except KeyError:
            store.close()
            raise InvalidInputFormat("Error near the Storm")

        requested_r.update_date = gltime.utcDateNow()

        store.commit()
        store.close()

    @transact
    def self_update(self, receiver_gus, receiver_dict):
        """
        This is the method called by a receiver for change/set their preference
        """
        pass

    @transact
    def admin_get_single(self, receiver_gus):
        """
        @return a receiverDescriptionDict
        """

        store = self.getStore('receiver - admin_get_single')

        # I didn't understand why, but NotOneError is not raised even if the search return None
        try:
            requested_r = store.find(Receiver, Receiver.receiver_gus == unicode(receiver_gus)).one()
        except NotOneError:
            store.close()
            raise ReceiverGusNotFound
        if requested_r is None:
            store.close()
            raise ReceiverGusNotFound

        retReceiver = requested_r._description_dict()

        store.close()
        return retReceiver


    @transact
    def admin_get_all(self):

        store = self.getStore('receiver - admin_get_all')

        all_r = store.find(Receiver)

        retVal = []
        for rcvr in all_r:
            retVal.append(rcvr._description_dict())

        store.close()
        return retVal


    @transact
    def full_receiver_align(self, context_gus, un_receiver_selected):
        """
        Called by Context handlers (PUT|POST), roll in all the receiver and delete|add|skip
        with the presence of context_gus
        """
        store = self.getStore('full_receiver_align')

        receiver_selected = []
        for r in un_receiver_selected:
            receiver_selected.append(str(r))

        presents_receiver = store.find(Receiver)

        debug_counter = 0
        for r in presents_receiver:

            # if is not present in receiver.contexts and is requested: add
            if r.contexts and not context_gus in r.contexts:
                if r.receiver_gus in receiver_selected:
                    debug_counter += 1
                    r.contexts.append(str(context_gus))

            # if is present in context.receiver and is not selected: remove
            if r.contexts and context_gus in r.contexts:
                if not r.receiver_gus in receiver_selected:
                    debug_counter += 1
                    r.contexts.remove(str(context_gus))

        log.debug("    ****   full_receiver_align in all receivers after %s has been set with %s: %d mods" %
                  ( context_gus, receiver_selected, debug_counter ) )

        store.commit()
        store.close()

    @transact
    def receiver_align(self, receiver_gus, context_selected):
        """
        Called by Receiver handler, (PUT|POST), just take the receiver and update the
        associated contexts
        """
        store = self.getStore('receiver_align')

        try:
            requested_r = store.find(Receiver, Receiver.receiver_gus == unicode(receiver_gus)).one()
        except NotOneError:
            store.close()
            raise ReceiverGusNotFound
        if requested_r is None:
            store.close()
            raise ReceiverGusNotFound

        requested_r.contexts = []
        for c in context_selected:
            requested_r.contexts.append(str(c))

        log.debug("    ++++   receiver_align in receiver %s with contexts %s" %
                  ( receiver_gus, str(context_selected) ) )

        store.commit()
        store.close()

    @transact
    def receiver_delete(self, receiver_gus):
        """
        Delete a receiver, or raise an exception if do not exist
        """
        store = self.getStore('receiver delete')

        try:
            requested_r = store.find(Receiver, Receiver.receiver_gus == unicode(receiver_gus)).one()
        except NotOneError:
            store.close()
            raise ReceiverGusNotFound
        if requested_r is None:
            store.close()
            raise ReceiverGusNotFound

        # log.info()
        store.remove(requested_r)
        store.commit()
        store.close()

    # being a method called by another @transact, do not require @transact
    # too, because otherwise the order is screwed
    def unlink_context(self, context_gus):
        """
        @param context_gus: context to be found and unassigned if present
        @return: number of receiver unassigned in the operation.
        This method is called when a context is deleted: all the receiver
        reference pointing on it, need to be unassigned
        ----- by hypothesis, here we can delete the receiver without a context
        """
        store = self.getStore('receiver unlink_context')

        # same consideration of Context.get_receivers: probably there are a more
        # efficient selection query, for search a context_gus in a list
        results = store.find(Receiver)

        unassigned_count = 0

        for r in results:

            if not r.contexts:
                continue

            if str(context_gus) in r.contexts:
                r.contexts.remove(str(context_gus))
                unassigned_count += 1

        store.commit()
        store.close()
        return unassigned_count

    # called by a trasnact, update last mod on self, called when a new Tip is present
    def update_timings(self):
        pass

    # this method import the remote received dict.
    # would be expanded with defaults value (if configured) and with checks about
    # expected fields. is called by new() and admin_update() (and self_update() not yet!)
    def _import_dict(self, source_rd):

        self.name = source_rd['name']
        self.description = source_rd['description']
        self.tags = source_rd['tags']
        self.know_languages = source_rd['languages']

        #self.notification_selected = source_rd['notification_selected']
        if source_rd['notification_selected'] or source_rd['notification_selected'] != "email":
            self.notification_fields = "email"
        else:
            print "** Receiver registered with unusual notification system"
            self.notification_fields = "email"

        self.notification_fields = source_rd['notification_fields']
        self.delivery_selected =  source_rd['delivery_selected']
        self.delivery_fields =  source_rd['delivery_fields']

        self.can_delete_submission = source_rd['can_delete_submission']
        self.can_postpone_expiration = source_rd['can_postpone_expiration']
        self.can_configure_delivery = source_rd['can_configure_delivery']
        self.can_configure_notification = source_rd['can_configure_notification']

        self.receiver_level = source_rd['receiver_level']

    # this is non @transact method used when is required to dump the objects
    # in a dict. The returned values should be removed using .pop(),
    def _description_dict(self):

        descriptionDict = {
            'receiver_gus' : self.receiver_gus,
            'name' : self.name,
            'description' : self.description,
            'tags' : self.tags if self.tags else [],
            'languages' : self.know_languages if self.know_languages else [],
            'notification_selected' : self.notification_selected,
            'notification_fields' : self.notification_fields,
            'delivery_selected' :  self.delivery_selected,
            'delivery_fields' :  self.delivery_fields,
            'creation_date' : gltime.prettyDateTime(self.creation_date),
            'update_date' : gltime.prettyDateTime(self.update_date),
            'last_access' : gltime.prettyDateTime(self.last_access),
            'contexts' : self.contexts if self.contexts else [],
            'receiver_level' : self.receiver_level,
            'can_delete_submission' : self.can_delete_submission,
            'can_postpone_expiration' : self.can_postpone_expiration,
            'can_configure_delivery' : self.can_configure_delivery,
            'can_configure_notification' : self.can_configure_notification
        }
        return descriptionDict


# Receivers are NEVER slippery: http://i.imgur.com/saLqb.jpg

