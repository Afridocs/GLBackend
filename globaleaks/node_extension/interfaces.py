from zope.interface import Interface

class IStorage(Interface):
    """
    Storage Interface return file hanler overriding the common file object,
    KEYWORDS:

        @resource: a directory, an identificative able to track multiple files
        @file: a unit of data
        @fileid: the identificative of the file
    """

    def storage_name():
        """
        XXX
        What does this do?
        Should this not be an attribute?
        """

    def get_admin_opt():
        """
        XXX
        What does this do?
        """

    def set_admin_opt(module_admin_config):
        """
        XXX
        What does this do?
        """

    def init():
        """
        this function is called at every start of GLBackend when
        the module has been configured and enabled.
        returning False here would be a FATAL error
        """

    def check_resource(resource):
        """
        return True if the resource exists, or False if not
        """

    def list_resource(resource):
        """
        return a list of the available ID in a resource
        """

    def secure_resource_delete(resource):
        """
        perform a secure delete of all files in a resource, and delete
        the resource reference. return True if successful.
        """

    def open_fileid(resource, fileid, seek):
        """
        perform an opening of a resource, return a 'file' object.
        move the flow to 'seek' index if present
        create the resource if not available
        """

    def get_fileid_stats():
        """
        return the actual seek index, a description of the supported
        feature, and the os.stat equivalent struct
        TO BE SPECIFIED
        """

    def secure_fileid_delete(resource, fileid):
        """
        perform a secure removal of file data and delete fileid
        reference, return True if sucessflul
        """

    def close_fileid():
        """
        close the 'file' and perform the completation of the I/O operation
        return True if successful
        """

