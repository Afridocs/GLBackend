# -*- coding: UTF-8
#   Answers
#   *******
#   :copyright: 2012 Hermes No Profit Association - GlobaLeaks Project
#   :author: Claudio Agosti <vecna@globaleaks.org>, Arturo Filastò <art@globaleaks.org>
#   :license: see LICENSE
#
#   This file contain the definition of all the answer struct perfomed by GLB
#   is used by curteg client (for verifiy that the answer fit with the expected format)
#   and by glbackend for format & sanitize output

from globaleaks.utils import recurringtypes as GLT

# This is the struct containing the errors
class errorMessage(GLT.GLTypes):

    def __init__(self, httpErrorCode=False, errorDict=False):
        """
        errorMessage may be used as inline object declaration and assignment
        """

        GLT.GLTypes.__init__(self, self.__class__.__name__)

        self.define("http_error_code", "int")
        self.define("error_code", "int")
        self.define("error_message", "string")
            # this is just a string, in the client the right
            # translated error, would be hooked using error_code

        if httpErrorCode:
            self.http_error_code = httpErrorCode

        if errorDict:
            self.error_code = errorDict.get('code')
            self.error_message = errorDict.get('message')

# U1
class nodeMainSettings(GLT.GLTypes):

    def __init__(self):

        GLT.GLTypes.__init__(self, self.__class__.__name__)

        self.define("name", "string")
        self.define("public_site", "string")
        self.define("hidden_service", "string")
        self.define("url_schema", "string")
        self.define("node_properties", GLT.nodePropertiesDict() )
        self.define("public_statistics", GLT.publicStatisticsDict() )
        self.define_array("contexts", GLT.contextDescriptionDict() )
        # self.define("description", localization) 
        # GlClient -- how would be handled the localization ?

# U2
class newSubmission(GLT.GLTypes):
    def __init__(self):
        GLT.GLTypes.__init__(self, self.__class__.__name__)
        self.define('submission_id', 'submissionID')
        self.define('creation_time', 'time')

# U3 
class submissionStatus(GLT.GLTypes):

    def __init__(self):

        GLT.GLTypes.__init__(self, self.__class__.__name__)

        self.define_array('fields', GLT.formFieldsDict(), 1)
        self.define_array('receivers', GLT.receiverDescriptionDict() )
        self.define('creation_time', 'time')

# U5
class finalizeSubmission(GLT.GLTypes):

    def __init__(self):

        GLT.GLTypes.__init__(self, self.__class__.__name__)
        self.define('receipt', 'receiptID')


# T1 use the base GLT.tipDetailsDict

# R1
class commonReceiverAnswer(GLT.GLTypes):

    def __init__(self):

        GLT.GLTypes.__init__(self, self.__class__.__name__)

        self.define("tips", GLT.tipIndexDict() )
        self.define("receiver_properties", GLT.receiverDescriptionDict() )

        self.define_array("notification_method", GLT.moduleDataDict() , 1)
        self.define_array("delivery_method", GLT.moduleDataDict() , 1)

# R2
class receiverModuleAnswer(GLT.GLTypes):

    def __init__(self):
        GLT.GLTypes.__init__(self, self.__class__.__name__)
        self.define_array("modules", GLT.moduleDataDict() )


# A1
class nodeMainSettings(GLT.GLTypes):

    def __init__(self):

        GLT.GLTypes.__init__(self, self.__class__.__name__)

        self.define("name", "string")
        self.define("admin_statistics", GLT.adminStatisticsDict() )
        self.define("public_statistics", GLT.publicStatisticsDict() )
        self.define("node_properties", GLT.nodePropertiesDict() )

        # self.define("node_description", GLT.localizationDict() )
        # localizationDict -- i need to understand how can be interfaced
        # with POT files

        self.define_array("contexts", GLT.contextDescriptionDict() )
        self.define("public_site", "string")
        self.define("hidden_service", "string")
        self.define("url_schema", "string")

# A2
class adminContextsCURD(GLT.GLTypes):
    def __init__(self):
        GLT.GLTypes.__init__(self, self.__class__.__name__)
        self.define_array("contexts", GLT.contextDescriptionDict() )

# A3
class adminReceiverCURD(GLT.GLTypes):
    def __init__(self):
        GLT.GLTypes.__init__(self, self.__class__.__name__)
        self.define_array("receivers", GLT.receiverDescriptionDict() )

# A4
class adminModulesUR(GLT.GLTypes):
    def __init__(self):
        GLT.GLTypes.__init__(self, self.__class__.__name__)
        self.define_array("modules", GLT.moduleDataDict() )
