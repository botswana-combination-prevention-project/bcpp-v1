import socket
from django.conf import settings
from bhp_common.utils import os_variables


class ContextDescriptor(object):

    """Descriptior for a template context"""

    def __init__(self, **kwargs):
        pass

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, arg):
        if isinstance(arg, dict):
            self.value = arg
        else:
            raise AttributeError("Attribute \'context\' must be type Dict. Got %s" % type(arg))


class BaseContext(object):

    values = ContextDescriptor()

    def __init__(self):
        try:
            main_app_label = settings.MAIN_APP_LABEL
        except:
            main_app_label = ''
        self.values = {
            "app_label": main_app_label,
            "hostname": socket.gethostname(),
            "os_variables": os_variables(),
            }

    def add_to_context(self, dct):
        self.add(dct)

    def add(self, **kwargs):
        """ add a k,v pair or update an existing k"""
        if kwargs:
            # k,v pairs should be passed only after you have initialized context
            for k, v in kwargs.items():
                self.values[k] = v
        #else:
        #    raise AttributeError, "Can't add to context, expected type dict. Got %s" % type(kwargs)

    def remove(self, key):
        """ remove existing key or raise error """
        if key in self.values.keys():
            del self.values[key]
        else:
            raise AttributeError("Can't \'remove\' dict key from context. Does not exist. Got key=%s" % key)

#    def remove_as_dictionary(self, arg):
#        if arg and isinstance(arg, dict):
#            del self.values[j]

    def remove_as_list(self, remove_keys):
        """ remove keys given a list of keys """
        if isinstance(remove_keys, list):
            for key in self.values.keys():
                if key in remove_keys:
                    del self.values[key]
        else:
            raise AttributeError("Method remove_as_list() expects arg to be type list. Got %s" % type(remove_keys))
