====================================
GlobaLeaks Helper class and function
====================================

1. `Files`_

    1. `utils`_
        1. `random_string`_
    2. `Receivers`_
    3. `datatypes`_
        1. `GlbFile`_
        4. `ModuleConf`_

Files
=====

`utils`_: contain utiliy function useful in various part of GLbackend logic.

`Receivers`_: Useful function The name of a single submission inside the GlobaLeaks system.

`datatypes`_: is the user which perform a submission, containing the information he want communicate outside.


utils
-----

contain utiliy function useful in various part of GLbackend logic, 

random_string
`````````````

return a cryptographically secure printable string, taking the parameters:

    :length: the length of the random string
    :type: needs to be passed as comma separated ranges or values,
           ex. "a-z,A-Z,0-9".


Receivers
---------

datatypes
---------

GlbFiles
````````

a class used to update the JSON object used to describe file via REST. the format expected by the client
is always:

file descriptor, every completed file upload is always stored and represented with this dict:

    { filename: <string>, comment: <String>, size: <Int, in bytes>, content-type: <string> }

methods and logic under review

ModuleConf
``````````
a class used to build the JSON object used in REST interaction with modules. The REST interfaces
using the ModuleConf generated JSON are:

`/receiver/<string t_id>/overview`

`/admin/receivers/`
`/admin/node`
`/admin/delivery`
`/admin/notification/`
`/admin/storage/`
`/admin/filtering`

And ModuleConf is usd inside the module of Delivery, Notification, Storage as JSON helper.

    ModuleConf(info <Dict: [ Module name <String>, Module description <String> ]>)

Instance the object with the descriptio

    add_bool(variabe name <String>, description <String>, default value <Bool>)
    add_password(variabe name <String>, description <String>, default value <String>)
    add_text(variabe name <String>, description <String>, default value <String>)

All the previous functions collect the requested field in a nested dict() construct, 
the nested dict as the form of:

[ fieldName, [ Type, Description, Default, Value ] ]

    get_json()

get_json return a JSON object based on the collected nested dict, the output is 
used in REST/GET function, for extract data form a resource and show them to the user.

Beside the value, it present also the default and the present value, this permit to
form a query fields, ready to be filled by the user.


    validate( JSON used to be show, JSON received)

The validate function is called after a REST/POST has new data for the resource,
validate compare the integrity of the submitted input, verify the types (string,
bool, int) and return a nested dict() representing the received input
