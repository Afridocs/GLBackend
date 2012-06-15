
class Delivery:

    def __init__(self):
        pass

    def notification_name(self):
        print "error: superclass never need to be called"

    def get_admin_opt(self):
        print "error: superclass never need to be called"

    def set_admin_opt(self, module_admin_config):
        pass

    def get_receiver_opt(self):
        pass

    def set_receiver_opt(self, module_data_struct):
        pass

    def do_notify(self, receiver, material):
        pass

    def get_log(self):
        pass
