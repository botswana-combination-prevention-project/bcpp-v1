import logging
from django.db.models import get_models
from django.core import serializers
from bhp_crypto.models import Crypt
from bhp_base_model.classes import BaseListModel

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class CheckoutController(object):
    def __init__(self, debug=False, netbook=None, site_code=None):
        self.debug = debug
        if netbook:
            self.netbook = netbook

    def set_netbook(self, netbook):
        if netbook:
            self.netbook = netbook
        else:
            raise ValueError("PLEASE specify the netbook you want checkout models to!")

    def update_crypt(self):
        """Grabs the entire crypt table from the "server" to the local device
        """
        if not self.netbook:
            raise ValueError("PLEASE specify the netbook you want checkout models to!")
        #print "Started! This will take a while ..."
        json = serializers.serialize(
            'json',
            Crypt.objects.using('default').filter(),
            use_natural_keys=True
            )
        for obj in serializers.deserialize("json", json):
            obj.save(using=self.netbook)

        #print "I'm done ..."

    def update_lists(self):
        """Updates all list models in "default" with data from "server".
        """
        #Make sure we have a target netbook to export lists to
        if not self.netbook:
            raise ValueError("PLEASE specify the netbook you want checkout models to!")
        list_models = []
        for model in get_models():
            if issubclass(model, BaseListModel):
                list_models.append(model)
        for list_model in list_models:
            print list_model._meta.object_name
            json = serializers.serialize(
                'json',
                list_model.objects.all().order_by('name'),
                use_natural_keys=True
                )

            for obj in serializers.deserialize("json", json):
                obj.save(using=self.netbook)

    def import_as_json(self, remote_instance, using="default"):
        """Serialize a remote model instance, deserialize and save to local instances.
            Args:
                remote_instance: a model instance from a remote server
                using: using parameter for the target server, default(default).
        """

        json = serializers.serialize('json', [remote_instance], use_natural_keys=True)
        for obj_new in serializers.deserialize("json", json, use_natural_keys=True):
            obj_new.save(using=using)
            print obj_new.object
        return remote_instance

