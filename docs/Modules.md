
## Notification and Delivery modules specification

GLBackend supports extension in classes 'Notification' and 'Delivery', 
those classes are called in two time:

  * by the task handler, are executed for every receiver with a new Tip associated.

  * by the event handler, when a new module is enabled by the adminitrator,
    this operation may not be completed if the adminitrator does not provide
    right configuration to the module

Notification and Delivery behaviour is like abstract classes, they
required extension and implementation by overriding methods.

The methods requird to be implemented by modules are:

class NotificationImplementation(Notification):

    def notification_name():
        """
        This method return the notification name, need to be different
        for every implementation, and the name will be associated with
        receivers preferences and settings, therefore shall never be
        changed in a running node
        """

    def get_admin_opt():
        return ModuleAdminConfig
        """
        ModuleAdminConfig is described in REST-spec.md
        """
    def set_admin_opt(ModuleAdminConfig):
        """
        During the setup of the module, if the admin need fill options,
        in get_ is returned the field struct, and in set is verify and
        recorded.
        """

    def get_receiver_opt(ModuleDataStruct):
        """
        ModuleDataStruct is described in REST-spec.md
        """
    def set_receiver_opt():
        return ModuleDataStruct
        """
        Same logic of admin_opt, but related for receiver specific 
        settings
        """

    def do_notify():
        """
        Called by the task handler, perform the notification, this option is
        called once for every receivers configured
        """

    def notification_complete():
        """
        Called when the last receiver has been handled, useful to 
        execute cleanup
        """

    def get_log():
        """
        The log are collected in Notification superclass, and returned 
        to the called using this function. When returned are flushed 
        by memory, permitting a centralized handling of the log
        """

class DeliveryImplementation(Delivery):
    """
    Delivery superclass behaviour is equal to Notification
    """

    def delivery_name():

    def get_admin_opt():
        return ModuleAdminConfig
    def set_admin_opt(ModuleAdminConfig):

    def get_receiver_opt(ModuleDataStruct):
    def set_receiver_opt():
        return ModuleDataStruct

    def do_delivery():
    def delivery_complete():
    def get_log():

## Storage modules specification
## Test under development

Try to abstract the 'file' concept: there are a container (folder),
with some univoke identified (filename) with data inside.

Storage Abstract class need to expose the following operations:

   get name of the plugin,

   init system environment 
     (checks distributed filesystem, checks database password)
     executed every time GLBackend start

   export confguration
     (every time admin is GETting module settings)
     <ModuleAdminConfig>


   get statistic about usage

   put a triple (folder, filename, file) in the storage
     (or: session-ID, fileID, file)
     (or: receiver-id, encryptted-filename, encrypted-file)
   get a file having the folder+filename
   get the list of filenames having a folder
   delete a file having the folder+filename
   delete a folder

### The test

Actually the idea is to wrap the File object, and return a File 
object from the method "get a file having folder+filename". This
may permit to relay on FileStream instead of huge memory buffer 
filled with binary data. This mean that all the storag operation
should be performed on standard File interface, but require just
a different open (get) and listing method.


## Filter modules specification

Filter abstract class need to expose the following operations:

    collect a file, contextualized by submission data (ID)
    by a datetime. a function that simply "collect", parse,
    extract metadata.

    get evaluation: True|False answer expressing the status
    of the analysis.

    get file modified: (Optional) if a file maybe modified by 
    the plugin and the evaluation has returned True, this
    function return 

### Plausible use for filter modules

  * antispam
  * antivirus checks on submitted file
  * metadata cleaning/extraction

