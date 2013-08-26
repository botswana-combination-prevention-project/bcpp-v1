import socket
import copy
from django.conf import settings
from bhp_common.utils import os_variables


class BaseContext(object):

    def __init__(self):
        self._items = {}
        self._default_items = None

    def get(self):
        return copy.deepcopy(self._get_items())

    def _set_default_items(self):
        self._default_items = {}
        try:
            main_app_label = settings.MAIN_APP_LABEL
        except:
            main_app_label = ''
        self._default_items.update({
            "app_label": main_app_label,
            "hostname": socket.gethostname(),
            "os_variables": os_variables(),
            })

    def _get_default_items(self):
        if not self._default_items:
            self._set_default_items()
        return copy.deepcopy(self._default_items)

    def set_items(self):
        self._items = {}
        self._items.update(self._get_default_items())

    def _get_items(self):
        if not self._items:
            self.set_items()
        return self._items

    def add(self, items=None, **kwargs):
        """ Add to the items either by passing a dictionary or keyword args or both"""
        if items:
            if not isinstance(items, dict):
                raise TypeError('Expected a dictionary. Got {0}'.format(items))
            self._get_items().update(items)
        if kwargs:
            self._get_items().update(kwargs)

    def remove(self, key):
        """ remove existing key or raise error """
        if key in self._get_items():
            del self._get_items()[key]
        else:
            raise AttributeError("Can't \'remove\' dict key from context. Does not exist. Got key=%s" % key)

    def remove_as_list(self, remove_keys):
        """ remove keys given a list of keys """
        if isinstance(remove_keys, list):
            for key in self._get_items():
                if key in remove_keys:
                    del self._get_items()[key]
        else:
            raise AttributeError("Method remove_as_list() expects arg to be type list. Got %s" % type(remove_keys))
