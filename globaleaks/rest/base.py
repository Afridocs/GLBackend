# -*- coding: UTF-8
# 
#   rest/base
#   *********
#
#   Contains all the logic handle input and output validation.

import inspect
import json
from datetime import datetime
from globaleaks.rest.errors import InvalidInputFormat

__all__ = ['validateMessages', 'GLTypes', 'SpecialType' ]

def validateType(value, valid_type):
    if type(value) is valid_type:
        return
    else:
        raise InvalidInputFormat("%s is not %s" % (value, str(valid_type) ) )

def validateGLType(value, gl_type):
    message = json.dumps(value)
    validateMessage(message, gl_type)

def validateSpecialType(value, specialType):
    """
    Validate a special type that is not in the standard types (int, str,
    unicode, etc.)
    """
    specialType.validate(value)

def validateItem(val, valid_type):
    """
    Takes as input an object and a type that it should match and raises an
    error if it does not match the type it is supposed to be.

    If there is still some processing to do it will call itself of
    validateMessage recursively to validate also the sub-elements.

    val: value to be to validated. This is a python object.

    valid_type: a subclass of GLTypes, SpecialType, type or list. This is what
    val should look like.
    """
    if type(valid_type) is list:
        if not type(val) is list:
            raise InvalidInputFormat("type(%s) = %s not list" % (str(val), type(val)) )
        valid = valid_type[0]
        for item in val:
            if type(item) is dict:
                validateGLType(item, valid)
            else:
                validateItem(item, valid)

    elif issubclass(valid_type, SpecialType):
        valid_type = valid_type()
        valid_type.validate(val)

    elif issubclass(valid_type, GLTypes):
        validateGLType(val, valid_type)

    elif type(valid_type) is type:
        validateType(val, valid_type)

    else:
        raise InvalidInputFormat(valid_type.__name__)


def validateMessage(message, message_type):
    """
    Takes a string that represents a JSON messages and checks to see if it
    conforms to the message type it is supposed to be.

    This message must be either a dict or a list. This function may be called
    recursively to validate sub-parameters that are also go GLType.

    message: the message string that should be validated

    message_type: the GLType class it should match.
    """
    messageSpec = message_type()

    obj = json.loads(message)
    return obj

    # ...
    #
    # if type(obj) is list:
    #     obj = obj.pop()
    # elif type(obj) is not dict:
    #     raise InvalidInputFormat("not list nor dict")

    # for k, val in obj.items():
    #     try:
    #         valid_type = messageSpec[k]
    #     except:
    #         raise InvalidInputFormat(k)

    #     validateItem(val, valid_type)
    # return obj

def validateWith(fn):
    """
    This is a decorator that does validation of the content in
    self.request.body and makes sure it is of the correct message_type.
    """
    def decorator(self, message_type):
        print "Validating"
        print self.request.body
        validateMessage(self.request.body, message_type)
        fn(self)
    return decorator



## Follow the base messages

class GLTypes(dict):
    """
    Types is a module supporting the recurring types format in JSON
    communications. It's documented in
    https://github.com/globaleaks/GlobaLeaks/wiki/recurring-data-types

    This class is used whenever a RESTful interface need to manage
    an input element or an output element.

    The recurring elements in GLBackend, researched here:
    https://github.com/globaleaks/GLBackend/issues/14
    and documented in https://github.com/globaleaks/GlobaLeaks/wiki/recurring-data-types
    are instances based on GLTypes
    """
    specification = {}
    def __getitem__(self, key):
        return self.specification[key]

    def __setitem__(self, key, val):
        self.specification[key] = val

    def __call__(self):
        return self.specification


class SpecialType(object):
    regexp = ""
    def validate(self, data):
        import re
        try:
            if re.match(self.regexp, data):
                return True
            else:
                raise InvalidInputFormat("failed regexp [%s] vs [%s]" % (self.regexp, data) )

        except TypeError:
            raise InvalidInputFormat("TypeError in regexp [%s] vs [%s]" % (self.regexp, data) )

class dateType(SpecialType):
    pass

class timeType(SpecialType):
    pass

class fileGUS(SpecialType):
    regexp = r"(f_[a-zA-Z]{20,20})"

# XXX not true anymore, need to be update the specification and the glossary
class receiptGUS(SpecialType):
    regexp = r"(\d{10,10})"

class submissionGUS(SpecialType):
    regexp = r"(s_[a-zA-Z]{50,50})"

class receiverGUS(SpecialType):
    regexp = r"(r_[a-zA-Z]{20,20})"

class profileGUS(SpecialType):
    regexp = r"(p_\d{10,10})"

class moduleENUM(SpecialType):
    regexp = "(notification|delivery|inputfilter)"

class contextGUS(SpecialType):
    regexp = r"(c_[a-zA-Z]{20,20})"

class commentENUM(SpecialType):
    regexp = r"(receiver|system|whistleblower)"

class tipGUS(SpecialType):
    regexp = r"(t_[a-zA-Z]{50,50})"

class fileDict(GLTypes):

    specification = {
            "name": unicode,
            "description": unicode,
            "size": int,
            "content_type": unicode,
            "date": dateType,
            "metadata_cleaned": bool,
            "completed": bool
    }

class receiverDescriptionDict(GLTypes):

    specification = {
            "gus": receiverGUS,
            "can_delete_submission": bool,
            "can_postpone_expiration": bool,
            "can_configure_notification": bool,
            "can_configure_delivery": bool,
            # -----------------------------------------
            "can_trigger_escalation": bool,
            "receiver_level": int,
            # remind: both of them need to be specified
            "name": unicode,
            "description": unicode,
            "tags": unicode,
            # verify - is it specified ?
            "creation_date": timeType,
            "last_update_date": timeType,
            # update the name
            "languages_supported": [unicode],
    }

class nodePropertiesDict(GLTypes):
    """
    Gradually this options has been shrinked because:
        1) threat model need to be completed
        2) some of them has been moved in the Contexts
        3) CBP are aimed in leakdirectory integration
    """
    specification = {"anonymous_submission_only": bool}

class adminStatisticsDict(GLTypes):
    """
    This containers need to be defined, IMHO would be an aggregate
    of information collected about the latest X-hours of the node
    and so far
    """
    specification = {
            "hours_interval": int,
            "download_number": int,
            "receiver_accesses": int,
            "submission_received": int
    }

class publicStatisticsDict(GLTypes):
    """
    The following container is used for the public statistic,
    collected by site that perform uptime and/or measurement,
    or readed by users.
    Need to be defined, depends what's is considered to be
    harmless for node life, and what's can be easily collected
    """
    specification = {
            "active_contexts": int,
            "active_receivers": int,
            "uptime_days": int
    }


class formFieldsDict(GLTypes):
    """
    field_type need to be defined as ENUM, in the future,
    and would be the set of keyword supported by the
    client (text, textarea, checkbox, GPS coordinate)
    """
    specification = {
            "presentation_order": "int",
            "label": unicode,
            "name": unicode,
            "required": bool,
            "hint": unicode,
            "value": unicode,
            "type": unicode}


class moduleDataDict(GLTypes):

    specification = {
            "profile_gus": profileGUS,
            "active": bool,
            "module_type": unicode,
            "name": unicode,
            "module_description": unicode,
            "service_message": unicode,
            "admin_fields": [formFieldsDict],
            "receiver_options": [formFieldsDict]
    }


class contextDescriptionDict(GLTypes):
    """
    fields: one or more, but almost one field is needed

    selectable_receiver:
        update, the previous flag before was documented as
        node-wise configuration, now is context-wise

    receivers: properties in Receiver element

    language_supported: it's the collection of Language from 'receivers'
    """
    specification = {
            "context_gus": contextGUS,
            "name": unicode,
            "description": unicode,
            "creation_date": timeType,
            "update_date": timeType,
            "fields": [ formFieldsDict ],
            "selectable_receiver": bool,
            "receivers": [receiverDescriptionDict],
            "escalation_threshold": int,
            "languages_supported": list
    }

class commentDescriptionDict(GLTypes):

    specification = {
            "writtentext": unicode,
            "commenttype": commentENUM,
            "author": unicode,
            "date": timeType
    }


class tipSubIndex(GLTypes):

    specification = {
            "tip_gus": tipGUS,
            "notification_adopted": unicode,
            "delivery_adopted": unicode,
            "download_limit": int,
            "access_limit": int,
            "access_performed": int,
            "expiration_date": timeType,
            "creation_date": timeType,
            "last_update_date": timeType,
            "comment_number": int,
            "files_number": int,
            "overall_pertinence": int
    }

class tipIndexDict(GLTypes):
    """
    Remind, this Tip access is different for every receiver,
    Remind: this object is the LIST OF ACTIVE TIP, does not
    cover the content.
    """
    specification = {
            "context_gus": contextGUS,
            "tiplist": [tipSubIndex]
    }

class tipDetailsDict(GLTypes):
    """
    This element contain mostly of the descriptive information
    of the Tip
    """

    specification = {
            "tip": tipSubIndex,
            "fields": formFieldsDict,
            "files": [fileGUS],
            "comments": commentDescriptionDict,
            "context": contextDescriptionDict,
            "receivers": receiverDescriptionDict
    }


class localizationDict(GLTypes):
    """
    This object would be implemented when localization would be solved
    as issue: https://github.com/globaleaks/GLBackend/issues/18
    """
    specification = {}


# https://github.com/globaleaks/GLClient/blob/master/app/scripts/dev.js#
# + filesGUS list: need to be added
# + complete boolean: because receipt can be proposed/received also before the
#   Submission has been finished.
# - folder_name and _description has been removed, because the scheduled and
#   InputFilter operation are performed on the single file.
# file are handled separately and XXX Architecture need to be updated about it.
class submissionStatus(GLTypes):

    specification = {
            "fields": [ formFieldsDict ],
            "context_selected": contextGUS,
            "submission_gus" : submissionGUS,
            "proposed_receipt": unicode,
            "files_description": unicode,
            "receiver_selected": [ receiverGUS ],
            "files_selected" : [ fileGUS ],
            "complete" : bool
    }



