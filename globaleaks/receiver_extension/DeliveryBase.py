# datatype include ModuleConf
from globaleaks.core.datatypes import *
from globaleaks.receiver_extension.Super import Delivery

class BaseDelivery(Delivery):

    def delivery_name(self):
        # TODO - need to be returned a Localized Dict
        return ("Base file download", "permit the receiver to download the material as compressed archive")

    def get_admin_opt(self):
        base_request = ModuleConf(self.delivery_name())
        base_request.add_bool('activate', 'Activate', True)
        base_request.add_bool('receiver-disable', 'Receiver can disable this option', False)
        base_request.add_bool('permit-password', 'Receiver can set a password to protect archives', True)
        return base_request.get_json()

    def set_admin_opt(self, json_admin_config):

        received_request = ModuleConf(self.delivery_name())

        if received_request.acquire(self.get_admin_opt(), json_admin_config) == True:
            # TODO - ORM dump
            return True
            # TODO - 200 HTTP and empty JSON
        else:
            return False
            # TODO - HTTP error as definied by REST-spec

    def get_receiver_opt(self):
        proposed_options = ModuleConf(self.delivery_name())

        # TODO - query the ORM about the admin options
        # DUMMY VALUE FOLLOWS
        configured_the_permit_password_TEMP = True
        configured_the_receiver_can_disable = False

        if configured_the_permit_password_TEMP == True:
            proposed_options.add_password('password', 'Set encryption password')

        if configured_the_receiver_can_disable == True:
            proposed_options.add_bool('active-by-receiver', 'Zip download', True)

        # is a dict, the returned value of ModuleConf
        return proposed_options.get_json()

    def set_receiver_opt(self, json_data_struct):
        received_request = ModuleConf(self.delivery_name())

        if received_request.acquire(self.get_receiver_opt(), json_data_struct) == True:
            # TODO - ORM dump
            return True
            # TODO - 200 HTTP and empty JSON
        else:
            return False

    def do_notify(self, receiver, material):
        """
        This method is called for every receiver, need to be implemented 
        when receiver and material ORM interaction are ready
        """
        pass


    def get_log(self):
        """
        To be implemented or discussed, when log management will be implemented
        """
        pass
