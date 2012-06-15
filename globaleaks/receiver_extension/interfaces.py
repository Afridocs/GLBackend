from zope.interface import Interface

class Delivery(Interface):

    def notification_name(self):
        """
        XXX
        Why is this not an attribute?
        """

    def get_admin_opt(self):
        """
        XXX
        Why is this not an attribute?
        """

    def set_admin_opt(self, module_admin_config):
        """
        XXX
        Why is this not an attribute?
        """

    def get_receiver_opt(self):
        """
        XXX
        Why is this not an attribute?
        """

    def set_receiver_opt(self, module_data_struct):
        """
        XXX
        Why is this not an attribute?
        """

    def do_notify(self, receiver, material):
        """
        XXX
        """

    def get_log(self):
        """
        XXX
        """
