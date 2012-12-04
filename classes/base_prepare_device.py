import logging
import socket
from uuid import uuid4
from datetime import datetime
from tastypie.models import ApiKey
from django.db.models import Q, Model, get_models, get_app, Max, Count
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission
from bhp_base_model.classes import BaseListModel
from bhp_userprofile.models import UserProfile
from bhp_content_type_map.classes import ContentTypeMapHelper
from base import Base


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BasePrepareDevice(Base):

    def __init__(self, using_source, using_destination, **kwargs):
        super(BasePrepareDevice, self).__init__(using_source, using_destination, **kwargs)

    def resize_content_type(self):
        """Resizes the destination content type table to have the same max id."""
        print '    Check django content type max id match on source and destination.'
        source_agg = ContentType.objects.using(self.get_using_source()).all().aggregate(Max('id'))
        destination_count = ContentType.objects.using(self.get_using_destination()).all().count()
        for n in range(1, source_agg.get('id__max') - destination_count):
            print '    {0} / {1} adding instance to django content_type.'.format(n, source_agg.get('id__max') - destination_count)
            ContentType.objects.using(self.get_using_destination()).create(app_label=str(uuid4()), model=str(uuid4()))

    def sync_content_type_map(self):
        """Runs content_type_map populate and sync on destination."""
        content_type_map_helper = ContentTypeMapHelper(self.get_using_destination())
        content_type_map_helper.populate()
        content_type_map_helper.sync()

    def update_api_keys(self, username=None):
        for user in User.objects.using(self.get_using_destination()).all():
            if not ApiKey.objects.using(self.get_using_destination()).filter(user=user):
                ApiKey.objects.using(self.get_using_destination()).create(user=user)
        if not username:
            username = 'django'
        # get username account api key
        source_api_key = ApiKey.objects.using(self.get_using_source()).get(user=User.objects.get(username=username))
        api_key = ApiKey.objects.using(self.get_using_destination()).get(user=User.objects.get(username=username))
        api_key.key = source_api_key.key
        api_key.save(using=self.get_using_destination())
        print '    updated {0}\'s api key on \'{1}\' to matching key on server.'.format(username, self.get_using_destination())
        print '    to update additional accounts use update_api_keys(source, destination, username).'.format(username, self.get_using_destination())

    def update_content_type(self):
        ContentType.objects.using(self.get_using_destination()).all().delete()
        self.update_model(ContentType, base_model_class=Model)

    def update_auth(self):
        UserProfile.objects.using(self.get_using_destination()).all().delete
        Permission.objects.using(self.get_using_destination()).all().delete
        User.objects.using(self.get_using_destination()).all().delete()
        Group.objects.using(self.get_using_destination()).all().delete()
        print '    update permissions'
        self.update_model(Permission, base_model_class=Model, use_natural_keys=False)
        print '    update groups'
        self.update_model(Group, base_model_class=Model, use_natural_keys=False)
        print '    update users'
        self.update_model(User, base_model_class=Model, use_natural_keys=False)
        print '    done with Auth.'

    def update_app_models(self, app_name):
        print '    updating for app {0}...'.format(app_name)
        models = []
        for model in get_models(get_app(app_name)):
            models.append(model)
        self.dispatch_model_as_json(models)

    def update_list_models(self):
        list_models = []
        print '    updating list models...'
        for model in get_models():
            if issubclass(model, BaseListModel):
                list_models.append(model)
        print '    found {0} list models'.format(len(list_models))
        for list_model in list_models:
            self.dispatch_model_as_json(list_model)
