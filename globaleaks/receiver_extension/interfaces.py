from zope.interface import Interface

"""
This is the skeleton class that may support delivery options in GLBackend,
This interface has been studied based on the prospect adopters of GLBackend,

To obtain a good knowledge transfert, I will use the following examples:

    1 a third party website with a growing community of uses that perform
      fact checking - document analysis - data revision.
      GLB provide anonymous interface for the whistleblower and has a
      REST interface for: 1) found the more appropiate receivers when required
      2) notify happen with a REST interface, and the delivery link is 
      provided (download are managed by GLB in this hypothesis)

    2 a company has different ticketing systems installed in the network
      and a safe GLB installation. for the different context selected,
      need a different authentication and REST to deliver the data in
      the appropriate system

    3 a simply WB site, with security feature offered for the receiver
      that want them.

      REFENRECE

    ModuleConf struct model is composed of:

    [ ModuleName, ModuleDescription,
      [ fieldName, fieldType, FieldDescription, FieldDefault, FieldValue]
      ...
    ]

    ModuleConf supports different field type (usually in the client association
    with different <input> element or different css/syle), actually has been
    provided:

    text (like <input type="text" />)
    immutable_text (every description, and some informative field)
    textarea (like <textarea /> ()
    bool (like <input type="checkbox" />)
    password (like <input type="password" />)

    Those field type need to be documented in the REST specification, because
    permit the client to handle dynamic resource easily.
"""

class Notification(Interface):

    def notification_name(self):
        """
        Notifiction name return a <LocaLDict>, containing the name of
        the extension and the short description, the short description
        NEED to be published in the admin interface and 
        MAYBE published in the receiver interface

        the LocaLDict is the localized data, making the users able to
        switch language directly from the client

        NO EXAMPLE PROVIDED HERE
        """
        pass

    def get_admin_opt(self):
        """
        Return the JSON containing the options useful for the admin.

        1 . Return a JSON struct based on ModuleConf, the admin need to setup the 
            interaction with the fact-checking website

            [ 'fact-checking-community-poll', 'this plugin blah blah',
              [ 'receiver-list-rest', 'text', 'write here the URL for get the BEST RECEIVERS list', None, None ]
            ]

        2. Return a JSON struct based on ModuleConf, the admin need to configure all the possible
           ticketing system present in the company

            [ 'lists-of-notification-system', 'this plugin blah blah corporate',
              [ 'ticketing1', 'text', 'write here the URL of system 1', None, None ]
              [ 'ticketing1-context', 'text', 'context handled by ticketing system 1', None, None ]
              [ 'ticketing2', 'text', 'write here the URL of system 1', None, None ]
              [ 'ticketing2-context', 'text', 'context handled by ticketing system 1', None, None ]
              ...
            ]

        3. Return a JSON struct based on ModuleConf, the admin choose if the security protection is 
           mandatory or not.
            [ 'receiver-security', 'Receiver can set public key protected notification',
              [ 'enable-gpg-enc', 'bool', 'Enable receiver in set GPG pubkey', False, None ]
              [ 'mandatory-gpg', 'bool', 'GPG key is mandatory', False, None ]
            ]
        """
        pass

    def set_admin_opt(self, module_admin_config):
        """
        This function receive the JSON struct compiled by the client.
        Case 3 example:

        3 .
            [ 'receiver-security', 'Receiver can set public key protected notification',
              [ 'enable-gpg-enc', 'bool', 'Enable receiver in set GPG pubkey', False, True ]
              [ 'mandatory-gpg', 'bool', 'GPG key is mandatory', False, True ]
            ]

        set_admin_opt perform the following operation:
        A) get_admin_opt take back the exaclty JSON struct sent to the user
        B) validate, check the integrity of the expected input (never trust the input!)
        C) acquire the value and save in the ORM, in this case, just two boolean are saved

        1 .
            [ 'fact-checking-community-poll', 'this plugin blah blah',
              [ 'receiver-list-rest', 'text', 'write here the URL for get the BEST RECEIVERS list', 
                 None, 'http://www.fact-checking.it/token=pipilotti/best-users/' ]
            ]

        """
        pass

    def get_receiver_opt(self):
        """
        This function return the JSON struct prepared based on the set_admin_option,
        The module description is the same

        3 . the admin has set the GPG key field and that this field is mandatory, the 
            recever option is dynamic based on what admin previously select.

            [ 'receiver-security', 'Receiver can set public key protection notification',
              [ 'key-id-configured', 'immutable_text', 'ID of your configured public key', None, None ]
              [ 'public-key', 'textarea', 'Your GPG key', None, None ]
            ]

            If a submit is performed with an empty 'public-key' field, the get_receiver_opt
            return an error.

        2 . the receiver has not any right to select the notification method,
            therfore get_receiver_opt return an empty ModuleConf object:

            [ 'lists-of-notification-system', 'this plugin blah blah corporate' ]

        1 . In the fact checking community example, an user may need to remove himself 
            from the list, of from a specific context:

            [ 'fact-checking-community-poll', 'this plugin blah blah',
              [ 'remove-me', 'bool', 'Remove from the list of document analysis', False, None ]
            ]

            REMOVE DETAIL: is already defined in the REST-spec the remove/suspend option for the
            receiver. in accessible for the receiver in /receiver/<t_id>/overview, where 
            the results of get_receiver_opt are printed.
        """
        pass

    def set_receiver_opt(self, module_data_struct):
        """

        This function accept the receiver option, and apply the same logic presented in 
        set_admin_opt:

        A) get_receiver_opt take back the exaclty JSON struct sent to the user
        B) validate, check the integrity of the expected input (never trust the input!)
        C) acquire the value and save in the ORM, recording booleand or text, and performing
           module dependend operation (in the GPG case: import the key, verify if is 
           a valid GPG public key)

        This function may return an appropriate error, or 200 when input is accepted.

        """
        pass

    def do_notify(self, receiver, data):
        """
        perform the notify, based on the configured options oof the admin (in set_admin_opt)
        and of the receiver if available (set_receiver_opt). 

        data is the information of the notification, here an email template, or a short message
        can be composed, encrypted, stored, forwarded, etc.
        """
        pass

    def check_receiver_conf(self, receiver):
        """
        A receiver may lack of the appropriate configuration. this would work for an admin
        overview, without invoke the do_notify function (if check_receiver_conf fail, also
        do_notify has to fail, but do_notify require a content)

        return True|False (HTTP error code 200 or 400)
        """

    def get_log(self):
        """
        logging need to be detaild, anyway the goal of a function here is that the 
        developer of the plugin has not to provide the various log level handling.

        has simply to collect log, with a log level, and then the GLBackend 
        task can aquire them, and treat as configured.
        """
        pass


class Delivery(Interface):
    """
    The concept are the same explained in Notification, simply delivery manage not 
    the uniqe link to the Tip, but the single material bulk uploaded by WB.
    """

    def delivery_name(self):
        """
        """
        pass

    def get_admin_opt(self):
        """
        """
        pass

    def set_admin_opt(self, module_admin_config):
        """
        """
        pass

    def get_receiver_opt(self):
        """
        """
        pass

    def set_receiver_opt(self, module_data_struct):
        """
        """
        pass

    def check_receiver_conf(self, receiver):
        """
        """
        pass

    def do_delivery(self, receiver, material):
        """
        """
        pass

    def get_log(self):
        """
        """
        pass


