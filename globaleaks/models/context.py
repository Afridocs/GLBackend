# -*- coding: UTF-8
#
#   models/context
#   **************
# 
# Implementation of the Storm DB side of context table and ORM

from storm.exceptions import NotOneError
from storm.twisted.transact import transact

from storm.locals import Int, Pickle
from storm.locals import Unicode, Bool, Date
from storm.locals import Reference

from globaleaks.utils import gltime, idops, log
from globaleaks.models.base import TXModel
from globaleaks.rest.errors import ContextGusNotFound, InvalidInputFormat

__all__ = [ 'Context' ]


class Context(TXModel):
    from globaleaks.models.node import Node

    __storm_table__ = 'contexts'

    context_gus = Unicode(primary=True)

    node_id = Int()
    node = Reference(node_id, Node.id)

    name = Unicode()
    description = Unicode()
    fields = Pickle()

    languages_supported = Pickle()

    selectable_receiver = Bool()
    escalation_threshold = Int()

    creation_date = Date()
    update_date = Date()
    last_activity = Date()

    tip_max_access = Int()
    tip_timetolive = Int()
    file_max_download = Int()

    # list of receiver_gus
    receivers = Pickle()

    # to be implemented in REST / dict
    notification_profiles = Pickle()
    delivery_profiles = Pickle()
    inputfilter_chain = Pickle()
    # to be implemented in REST / dict

    # public stats reference
    # private stats reference

    @transact
    def new(self, context_dict):
        """
        @param context_dict: a dictionary containing the expected field of a context,
                is called and define as contextDescriptionDict
        @return: context_gus, the universally unique identifier of the context
        """
        log.debug("[D] %s %s " % (__file__, __name__), "Context new", context_dict)

        store = self.getStore('context new')

        cntx = Context()

        cntx.context_gus = idops.random_context_gus()
        cntx.node_id = 1

        cntx.creation_date = gltime.utcDateNow()
        cntx.update_date = gltime.utcDateNow()
        cntx.last_activity = gltime.utcDateNow()
        cntx.receivers = []

        try:
            cntx._import_dict(context_dict)
        except KeyError:
            store.rollback()
            store.close()
            raise InvalidInputFormat("Import failed near the Storm")

        store.add(cntx)
        log.msg("Created context %s at the %s" % (cntx.name, cntx.creation_date) )
        store.commit()
        store.close()

        # return context_dict
        return cntx.context_gus

    @transact
    def update(self, context_gus, context_dict):
        """
        @param context_gus: the universal unique identifier
        @param context_dict: the information fields that need to be update, here is
            supported to be already validated, sanitized and logically verified
            by handlers
        @return: None or Exception on error
        """
        log.debug("[D] %s %s " % (__file__, __name__), "Context update of", context_gus)
        store = self.getStore('context update')

        try:
            requested_c = store.find(Context, Context.context_gus == unicode(context_gus)).one()
        except NotOneError:
            store.close()
            raise ContextGusNotFound
        if requested_c is None:
            store.close()
            raise ContextGusNotFound

        try:
            requested_c._import_dict(context_dict)
        except KeyError:
            store.rollback()
            store.close()
            raise InvalidInputFormat("Import failed near the Storm")

        requested_c.update_date = gltime.utcDateNow()

        store.commit()
        log.msg("Updated context %s in %s, created in %s" %
                (requested_c.name, requested_c.update_date, requested_c.creation_date) )

        store.close()

    @transact
    def delete_context(self, context_gus):
        """
        @param context_gus: the universal unique identifier of the context
        @return: None if is deleted correctly, or raise an exception if something is wrong.
        """
        from globaleaks.models.receiver import Receiver
        log.debug("[D] %s %s " % (__file__, __name__), "Context delete of", context_gus)

        # first, perform existence checks, this would avoid continuous try/except here
        if not self.exists(context_gus):
            raise ContextGusNotFound

        # delete all the reference to the context in the receivers
        receiver_iface = Receiver()

        # this is not a yield because getStore is not yet called!
        unlinked_receivers = receiver_iface.unlink_context(context_gus)

        # TODO - delete all the tips associated with the context
        # TODO - delete all the jobs associated with the context
        # TODO - delete all the stats associated with the context
        # TODO - align all the receivers present in self.receivers

        store = self.getStore('context delete')

        try:
            requested_c = store.find(Context, Context.context_gus == unicode(context_gus)).one()
        except NotOneError:
            store.close()
            raise ContextGusNotFound
        if requested_c is None:
            store.close()
            raise ContextGusNotFound

        store.remove(requested_c)
        store.commit()
        store.close()

        log.msg("Deleted context %s, created in %s used by %d receivers" %
                (requested_c.name, requested_c.creation_date, unlinked_receivers) )


    @transact
    def admin_get_single(self, context_gus):
        """
        @param context_gus: UUID of the contexts
        @return: the contextDescriptionDict requested, or an exception if do not exists
        """
        store = self.getStore('context admin_get_single')

        try:
            requested_c = store.find(Context, Context.context_gus == unicode(context_gus)).one()
        except NotOneError:
            store.close()
            raise ContextGusNotFound
        if requested_c is None:
            store.close()
            raise ContextGusNotFound

        ret_context_dict = requested_c._description_dict()

        store.close()
        return ret_context_dict

    @transact
    def admin_get_all(self):
        """
        @return: an array containing all contextDescriptionDict
        """
        log.debug("[D] %s %s " % (__file__, __name__), "Context admin_get_all")

        store = self.getStore('context admin_get_all')

        result = store.find(Context)

        ret_contexts_dicts = []
        for requested_c in result:
            ret_contexts_dicts.append( requested_c._description_dict() )

        store.close()
        return ret_contexts_dicts

    @transact
    def public_get_single(self, context_gus):
        """
        @param context_gus: requested context
        @return: context dict, stripped of the 'reserved' info
        """
        store = self.getStore('context public_get_single')

        try:
            requested_c = store.find(Context, Context.context_gus == unicode(context_gus)).one()
        except NotOneError:
            store.close()
            raise ContextGusNotFound
        if requested_c is None:
            store.close()
            raise ContextGusNotFound

        ret_context_dict = requested_c._description_dict()
        # remove the keys private in the public diplay of node informations
        ret_context_dict.pop('tip_max_access')
        ret_context_dict.pop('tip_timetolive')
        ret_context_dict.pop('file_max_download')
        ret_context_dict.pop('escalation_threshold')

        store.close()
        return ret_context_dict

    @transact
    def public_get_all(self):
        log.debug("[D] %s %s " % (__file__, __name__), "Context public_get_all")

        store = self.getStore('context public_get_all')

        ret_contexts_dicts = []
        result = store.find(Context)
        # also "None" is fine: simply is returned an empty array

        for requested_c in result:

            description_dict = requested_c._description_dict()
            # remove the keys private in the public diplay of node informations
            description_dict.pop('tip_max_access')
            description_dict.pop('tip_timetolive')
            description_dict.pop('file_max_download')
            description_dict.pop('escalation_threshold')

            ret_contexts_dicts.append(description_dict)

        store.close()
        return ret_contexts_dicts

    @transact
    def count(self):
        """
        @return: the number of contexts. Not used at the moment
        """
        store = self.getStore('context count')
        contextnum = store.find(Context).count()
        store.close()
        return contextnum

    # called always by transact method, from models
    def exists(self, context_gus):
        """
        @param context_gus: check if the requested context exists or not
        @return: True if exist, False if not, do not raise exception.
        """
        log.debug("[D] %s %s " % (__file__, __name__), "Context exists ?", context_gus)

        store = self.getStore('context exist')

        try:
            requested_c = store.find(Context, Context.context_gus == unicode(context_gus)).one()

            if requested_c is None:
                retval = False
            else:
                retval = True

        except NotOneError:
            retval = False

        store.close()
        return retval

    @transact
    def update_languages(self, context_gus):

        log.debug("[D] %s %s " % (__file__, __name__), "update_languages ", context_gus)

        language_list = []

        # for each receiver check every languages supported, if not
        # present in the context declared language, append on it
        for rcvr in self.get_receivers('internal', context_gus):
            for language in rcvr.get('know_languages'):
                if not language in language_list:
                    language_list.append(language)

        store = self.getStore('context update_languages')
        requested_c = store.find(Context, Context.context_gus == unicode(context_gus)).one()
        log.debug("[L] before language update, context", context_gus, "was", requested_c.languages_supported, "and after got", language_list)

        requested_c.languages_supported = language_list
        requested_c.update_date = gltime.utcDateNow()

        store.commit()
        store.close()

    # this is called internally by a @transact functions
    def get_receivers(self, info_type, context_gus=None):
        """
        @param context_gus: target context to be searched between receivers, if not specified,
            the receivers returned are searched in 'self'
        @info_type: its a string with three possible values:
           'public': get the information represented to the WB and in public
           'internal': a series of data used by internal calls
           'admin': complete dump of the information, wrap Receiver._description_dict
        @return: a list, 0 to MANY receiverDict tuned for the caller requirements
        """
        from globaleaks.models.receiver import Receiver

        typology = [ 'public', 'internal', 'admin' ]

        if not info_type in typology:
            log.debug("[Fatal]", info_type, "not found in", typology)
            raise NotImplementedError

        store = self.getStore('context get_receivers')

        # I've made some experiment with https://storm.canonical.com/Manual#IN (in vain)
        # the goal is search which context_gus is present in the Receiver.contexts
        # and then work in the selected Receiver.


        if context_gus:
            workinobj = store.find(Context, Context.context_gus == unicode(context_gus)).one()
        else:
            workinobj = self

        # Hi. I'm a really DIRTY HACK.
        # :)
        # Hi. I'm a really DIRTY HACK.
        # :)

        receiver_list = workinobj.receivers
        #store.close()
        #return receiver_list

        all_r = store.find(Receiver)
        for r in all_r:

            partial_info = {}

            if info_type == typology[0]: # public
                partial_info.update({'receiver_gus' : r.receiver_gus })
                partial_info.update({'name': r.name })
                partial_info.update({'description': r.description })
            if info_type == typology[1]: # internal
                partial_info.update({'receiver_gus' : r.receiver_gus })
                partial_info.update({'know_languages' : r.know_languages })
            if info_type == typology[2]: # admin
                partial_info = r._description_dict()

            receiver_list.append(partial_info)

        # GoodBye. I'm a really DIRTY HACK.
        # :)
        # GoodBye. I'm a really DIRTY HACK.
        # :)

        store.close()
        return receiver_list


    @transact
    def full_context_align(self, receiver_gus, un_context_selected):
        """
        Called by Receiver handlers (PUT|POST), roll in all the context and delete|add|skip
        with the presence of receiver_gus
        """
        store = self.getStore('full_context_align')

        context_selected = []
        for c in un_context_selected:
            context_selected.append(str(c))

        presents_context =  store.find(Context)

        debug_counter = 0
        for c in presents_context:

            # if is not present in context.receivers and is requested: add
            if c.receivers and not receiver_gus in c.receivers:
                if c.context_gus in context_selected:
                    debug_counter += 1
                    c.receivers.append(str(receiver_gus))

            # if is present in receiver.contexts and is not selected: remove
            if c.receivers and (receiver_gus in c.receivers):
                if not c.context_gus in context_selected:
                    debug_counter += 1
                    c.receivers.remove(str(receiver_gus))

        log.debug("    %%%%   full_context_align in all contexts after %s has been set with %s: %d mods" %
                  ( receiver_gus, str(context_selected), debug_counter ) )

        store.commit()
        store.close()


    @transact
    def context_align(self, context_gus, receiver_selected):
        """
        Called by Context handler, (PUT|POST), just take the context and update the
        associated receivers
        """
        store = self.getStore('context_align')

        try:
            requested_c = store.find(Context, Context.context_gus == unicode(context_gus)).one()
        except NotOneError:
            store.close()
            raise ContextGusNotFound
        if requested_c is None:
            store.close()
            raise ContextGusNotFound

        requested_c.receivers = []
        for r in receiver_selected:
            requested_c.receivers.append(str(r))

        log.debug("    ++++   context_align in receiver %s with receivers %s" %
                  ( context_gus, str(receiver_selected) ) )

        store.commit()
        store.close()

    # This is not a transact method, is used internally by this class to assembly
    # response dict. This method return all the information of a context, the
    # called using .pop() should remove the 'confidential' value, if any
    def _description_dict(self):

        description_dict = {
            "context_gus": self.context_gus,
            "name": self.name,
            "description": self.description,
            "selectable_receiver": self.selectable_receiver,
            "languages": self.languages_supported if self.languages_supported else [],
            'tip_max_access' : self.tip_max_access,
            'tip_timetolive' : self.tip_timetolive,
            'file_max_download' : self.file_max_download,
            'escalation_threshold' : self.escalation_threshold,
            'fields': self.fields,
            'receivers' : self.receivers if self.receivers else []

        }
        # receivers is added

        return description_dict

    # this method import the remote received dict.
    # would be expanded with defaults value (if configured) and with checks about
    # expected fields. is called by new() and update()

    def _import_dict(self, context_dict):

        self.name = context_dict['name']
        self.fields = context_dict['fields']
        self.description = context_dict['description']
        self.selectable_receiver = context_dict['selectable_receiver']
        self.escalation_threshold = context_dict['escalation_threshold']
        self.tip_max_access = context_dict['tip_max_access']
        self.tip_timetolive = context_dict['tip_timetolive']
        self.file_max_download = context_dict['file_max_download']

        if self.selectable_receiver and self.escalation_threshold:
            log.msg("[!] Selectable receiver feature and escalation threshold can't work both: threshold ignored")
            self.escalation_threshold = 0

