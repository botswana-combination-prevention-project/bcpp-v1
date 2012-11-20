import logging
from uuid import uuid4
from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from django.core.serializers.base import DeserializationError
from django.db.models import Model, get_model, get_models, get_app, Max
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission
from bhp_base_model.classes import BaseListModel, BaseModel
from bhp_userprofile.models import UserProfile


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class EdcDevicePrep(BaseCommand):
    APP_NAME = 0
    MODEL_NAME = 1

    def resize_content_type(self, using_source, using_destination):
        """Resizes the destination content type table to have the same max id."""
        print 'Check django content type max id match on source and destination.'
        source_agg = ContentType.objects.using(using_source).all().aggregate(Max('id'))
        destination_count = ContentType.objects.using(using_destination).all().count()
        for n in range(1, source_agg.get('id__max') - destination_count):
            print '    {0} / {1} adding instance to django content_type.'.format(n, source_agg.get('id__max') - destination_count)
            ContentType.objects.using(using_destination).create(app_label=str(uuid4()), model=str(uuid4()))

    def update_content_type(self, using_source, using_destination):
        ContentType.objects.using(using_destination).all().delete()
        self.update_model(ContentType, using_source, using_destination, base_model_class=Model)

    def update_auth(self, using_source, using_destination):
        UserProfile.objects.using(using_destination).all().delete
        Permission.objects.using(using_destination).all().delete
        User.objects.using(using_destination).all().delete()
        Group.objects.using(using_destination).all().delete()
        print '    update permissions'
        self.update_model(Permission, using_source, using_destination, base_model_class=Model, use_natural_keys=False)
        print '    update groups'
        self.update_model(Group, using_source, using_destination, base_model_class=Model, use_natural_keys=False)
        print '    update users'
        self.update_model(User, using_source, using_destination, base_model_class=Model, use_natural_keys=False)
        print '    done with Auth.'

    def update_app_models(self, app_name, using_source, using_destination):
        print 'Updating for app {0}...'.format(app_name)
        models = []
        for model in get_models(get_app(app_name)):
            models.append(model)
        self.import_as_json(models, using_source, using_destination)

    def update_model(self, model, using_source, using_destination, **kwargs):
        self.import_as_json(model, using_source, using_destination, **kwargs)

    def update_list_models(self, using_source, using_destination):
        list_models = []
        print 'Updating list models...'
        for model in get_models():
            if issubclass(model, BaseListModel):
                list_models.append(model)
        print '    found {0} list models'.format(len(list_models))
        for list_model in list_models:
            self.import_as_json(list_model, using_source, using_destination)

    def import_as_json(self, models, using_source, using_destination, **kwargs):
        """Serializes and saves all instances of each model from source to destination.

            Args:
                models: may be a tuple of (app_name, model_name) or list of model classes.
        """
        base_model_class = kwargs.get('base_model_class', BaseModel)
        use_natural_keys = kwargs.get('use_natural_keys', True)
        if not models:
            raise CommandError('Parameter \'models\' may not be None.')
        # if models is a tuple, convert to model class using get_model
        if isinstance(models, tuple):
            mdl = get_model(models[self.APP_NAME], models[self.MODEL_NAME])
            if not mdl:
                raise CommandError('Unable to get_model() using app_name={0}, model_name={1}.'.format(models[self.APP_NAME], models[self.MODEL_NAME]))
            models = mdl
        # models must be a list
        if not isinstance(models, (list,)):
            models = [models]
        for model in models:
            if not issubclass(model, base_model_class):
                raise CommandError('Parameter \'model\' must be an instance of BaseModel. Got {0}'.format(model))

            tot = model.objects.using(using_source).all().count()

            print '   saving {0} instances for {1} on {2}.'.format(tot, model._meta.object_name, using_destination)
            json = serializers.serialize('json', model.objects.using(using_source).all().order_by('id'), use_natural_keys=use_natural_keys)
            n = 0
            if json:
                try:
                    for obj in serializers.deserialize("json", json):
                        n += 1
                        obj.save(using=using_destination)
                except DeserializationError:
                    for instance in model.objects.using(using_source).all().order_by('id'):
                        json = serializers.serialize('json', [instance], use_natural_keys=True)
                        try:
                            for obj in serializers.deserialize("json", json):
                                n += 1
                                obj.save(using=using_destination)
                        except:
                            print '    SKIPPING {0}'.format(instance._meta.object_name)
            print '   done. saved {0} / {1} for model {2}'.format(n, tot, model._meta.object_name)


