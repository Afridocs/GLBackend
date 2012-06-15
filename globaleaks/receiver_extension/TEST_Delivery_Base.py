from globaleaks.core import datatypes
from globaleaks.receiver_extension.Delivery_Base import *

testB = BaseDelivery()

print "Class name: "
print testB.delivery_name()
print "\n"

adminreq = testB.get_admin_opt()

print "Admin json requested value: "
print adminreq
print "\n"

receiverreq = testB.get_receiver_opt()

print "Receiver json requested value:"
print receiverreq
print "\n"

admin_request = {"permit-password",  True }
if testB.set_admin_opt(admin_request) == True:
    print "set_admin with " + str(admin_request) + " accepted"
else:
    print "set_admin with " + str(admin_request) + " not accepted"


receiver_request = {"password": "forcaiolanda" }
if testB.set_receiver_opt(receiver_request) == True:
    print "set_receiver with " + str(receiver_request) + " accepted"
else:
    print "set_receiver with " + str(receiver_request) + " not accepted"



# {"checkbox": "permit-password", "default": true, "service-message": "permit the receiver to download the material as compressed archive", "module-name": "Base file download", "desc": "Receiver can set a password to protect archives"}
# {"default": null, "desc": "Set encryption password", "password": "password", "service-message": "permit the receiver to download the material as compressed archive", "module-name": "Base file download"}


