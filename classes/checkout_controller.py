import logging
from django.core import serializers
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.db.models import get_models, get_app, ForeignKey, OneToOneField
from bhp_visit_tracking.models import BaseVisitTracking
from bhp_crypto.models import Crypt
from bhp_base_model.classes import BaseListModel

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class CheckoutController(object):

    VISIT_MODEL_FLD = 0
    VISIT_MODEL_CLS = 1

    def __init__(self, debug=False, netbook=None, site_code=None):
        self.dispatch_list = []
        self.debug = debug
        self.netbook = None
        if netbook:
            self.netbook = netbook

    def set_netbook(self, netbook):
        if netbook:
            self.netbook = netbook
        else:
            raise ValueError("PLEASE specify the netbook you want checkout models to!")

    def update_crypt(self):
        """Gets the entire crypt table from the "server" to the local device
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

    def _set_visit_model_cls(self, app_name, model_cls):
        if not model_cls:
            raise TypeError('Parameter model_cls cannot be None.')
        for field in model_cls._meta.fields:
            if isinstance(field, ForeignKey):
                field_cls = field.rel.to
                if issubclass(field_cls, BaseVisitTracking):
                    self.visit_models.update({app_name: (field.name, field_cls)})

    def _get_visit_model_cls(self, app_name, model_cls=None):
        if not self.visit_models.get(app_name):
            self._set_visit_model_cls(app_name, model_cls)
        if not self.visit_models.get(app_name):
            return (None, None)
        return self.visit_models.get(app_name)

    def _export_foreign_key_models(self, app_name):
        """Finds foreignkey model classes other than the visit model class and exports the instances."""
        list_models = []
        if not app_name:
            raise TypeError('Parameter app_name cannot be None.')
        app = get_app(app_name)
        for model_cls in get_models(app):
            visit_field_name, visit_model_cls = self._get_visit_model_cls(app_name, model_cls)
            if getattr(model_cls, visit_field_name, None):
                for field in model_cls._meta.fields:
                    if not field.name == visit_field_name and isinstance(field, (ForeignKey, OneToOneField)):
                        field_cls = field.rel.to
                        if field_cls not in list_models:
                            list_models.append(field_cls)
        for model_cls in list_models:
            self.export_as_json(model_cls.objects.all(), self.netbook, app_name=app_name)

    def _get_scheduled_models(self, app_name):
        """Returns a list of model classes with a key to SubjectVisit excluding audit models."""
        app = get_app(app_name)
        # self._export_foreign_key_models(self, app_name)
        subject_model_cls = []
        for model_cls in get_models(app):
            field_name, visit_model_cls = self._get_visit_model_cls(app_name, model_cls)
            if visit_model_cls:
                if getattr(model_cls, field_name, None):
                    if not model_cls._meta.object_name.endswith('Audit'):
                        subject_model_cls.append(model_cls)
#        subject_model_names = ['Qn001', 'Qn002', 'SubjectArtHistory', 'SubjectAbsenteeReport', 'Locator', 'Qn001SectionTwo', 'Qn002SectionOne', 'Qn002SectionTwo', 'Qn002SectionThree', 'Qn002SectionFour', 'Qn002SectionFive', 'Qn002SectionSix', 'Qn002SectionSeven', 'Qn002SectionEightIntro', 'Qn002SectionEightPartnerRecent', 'Qn002SectionEightPartnerSecond', 'Qn002SectionEightPartnerThird']
#        subject_models = []
#        for model_name in subject_model_names:
#            model = get_model('mochudi_subject', model_name)
#            subject_models.append(model)
        return subject_model_cls

    def update_lists(self):
        """Update all list models in "default" with data from "server".
        """
        #Make sure we have a target netbook to export lists to
        if not self.netbook:
            raise ValueError("PLEASE specify the netbook you want checkout models to!")
        list_models = []
        for model in get_models():
            if issubclass(model, BaseListModel):
                list_models.append(model)
        for list_model in list_models:
            logger.info(list_model._meta.object_name)
            json = serializers.serialize(
                'json',
                list_model.objects.all().order_by('name'),
                use_natural_keys=True
                )

            for obj in serializers.deserialize("json", json):
                obj.save(using=self.netbook)

    def export_as_json(self, export_instances, using=None, **kwargs):
        """Serialize a remote model instance, deserialize and save to local instances.
            Args:
                remote_instance: a model instance from a remote server
                using: using parameter for the target server, default(default).
        """
        app_name = kwargs.get('app_name', None)
        if using:
            if using == 'default':
                raise TypeError('Cannot export to database \'default\' (using).')
            if export_instances:
                if not isinstance(export_instances, (list, QuerySet)):
                    export_instances = [export_instances]
                json = serializers.serialize('json', export_instances, use_natural_keys=True)
                for obj_new in serializers.deserialize("json", json, use_natural_keys=True):
                    try:
                        obj_new.save(using=using)
                    except IntegrityError:
                        if app_name:
                            # assume Integrity error is because of missing ForeignKey data
                            self._export_foreign_key_models(app_name)
                            # try again
                            obj_new.save(using=using)
                        else:
                            raise
                    except:
                        raise
                    logger.info(obj_new.object)
