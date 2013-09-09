import logging
from uuid import uuid4
from tastypie.models import ApiKey
from django.db import IntegrityError
from django.db.models import Model, get_model, get_models, get_app, Max, ForeignKey, OneToOneField
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission
from bhp_base_model.models import BaseListModel
from bhp_userprofile.models import UserProfile
from bhp_content_type_map.classes import ContentTypeMapHelper
from base_controller import BaseController


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BasePrepareDevice(BaseController):

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
        self.update_model(ContentType, [Model])

    def update_auth(self):
        UserProfile.objects.using(self.get_using_destination()).all().delete
        Permission.objects.using(self.get_using_destination()).all().delete
        User.objects.using(self.get_using_destination()).all().delete()
        Group.objects.using(self.get_using_destination()).all().delete()
        print '    update permissions'
        self.update_model(Permission, [Model])
        print '    update groups'
        self.update_model(Group, [Model])
        print '    update users'
        self.update_model(User, [Model])
        print '    done with Auth.'

    def update_app_models(self, app_name, additional_base_model_class=None):
        print '    updating for app {0}...'.format(app_name)
        #models = []
        for model in get_models(get_app(app_name)):
            #models.append(model)
            self.model_to_json(model, additional_base_model_class)

    def update_list_models(self):
        list_models = []
        print '    updating list models...'
        for model in get_models():
            if issubclass(model, BaseListModel):
                list_models.append(model)
        print '    found {0} list models'.format(len(list_models))
        for list_model in list_models:
            self.model_to_json(list_model)

    def reset_model(self, model_cls):
        """Deletes all instances of the given model and its audit log entries."""
        if not model_cls:
            raise TypeError('Please provide a model to delete.')
        using = self.get_using_destination()
#        print '    deleting {0}...'.format(model_cls._meta.object_name)
#        try:
#            self.reset_model_raw_sql(model_cls)
#            if "history" in dir(model_cls):
#                if model_cls.history.using(using).all().count() > 0:
#                    self.delete_audit_instances(model_cls)
#
#        except IntegrityError as e:
#            logger.info(e)
#            if 'Cannot delete or update a parent row' in e.args[1]:
#                if '_audit' in e.args[1]:
#                    # assume Integrity error was because of an undeleted related Audit model
#                    self.delete_audit_instances(model_cls)
#                    self.reset_model_raw_sql(model_cls)
#                else:
#                    self.delete_depended_model_instances(model_cls)
# #                    self.reset_model_raw_sql(model_cls)
#                    if "history" in dir(model_cls):
#                        if model_cls.history.using(using).all().count() > 0:
#                            self.delete_audit_instances(model_cls)
        for instance in model_cls.objects.using(using).all():
            print '    deleting {0}...'.format(instance)
            try:
                # Delete all the audit logs for the model
                # self.reset_model(model_cls)
                if "history" in dir(model_cls):
                    if model_cls.history.using(using).all().count() > 0:
                        self.delete_audit_instances(model_cls)
                    instance.delete(using=using)
                    print '    {0} -> {1} deleted..'.format(instance._meta.object_name, instance)
            except IntegrityError as e:
                logger.info(e)
                if 'Duplicate' in e.args[1]:
                    pass
                elif 'Cannot delete or update a parent row' in e.args[1]:
                    if '_audit' in e.args[1]:
                        # assume Integrity error was because of an undeleted related Audit model
                        self.delete_audit_instances(model_cls)
                        instance.delete(using=using)
                    else:
                        self.delete_depended_model_instances(model_cls)
                        instance.delete(using=using)
                elif 'Cannot add or update a child row' in e.args[1]:
                    if '_audit' in e.args[1]:
                        raise
                    else:
                        raise
                else:
                    raise
            except:
                    raise

    def delete_depended_model_instances(self, model_cls):
        """ Deletes all scheduled and visit models that depend on the given model"""
#        app_name = model_cls._meta.app_label
        for model in self.get_depended_models(model_cls):
            self.reset_model(model)

    def get_depended_models(self, fk_cls):
        """Returns a list of scheduled and visit models that depend
        (ForeignKey,OneToOneField) of the given model
        """
        _models = []
#        if not app_name:
#            raise TypeError('Parameter app_name cannot be None.')
#        app = get_app(app_name)
#        models = get_models(app)
        membershipform_models = self.helper.get_membershipform_models()
        scheduled_models = self.helper.get_scheduled_models()
        form_models = membershipform_models + scheduled_models
        '''For each visit and membership model check if it has a field that is a
        foreignkey or oneToone to the given model
         '''
        for model_cls in form_models:
            for field in model_cls._meta.fields:
                if  isinstance(field, (ForeignKey, OneToOneField)):
                    if field.rel.to == fk_cls:
                        if model_cls not in _models:
                            _models.append(model_cls)
        return _models

    def delete_audit_instances(self, model_cls):
        using = self.get_using_destination()
        print "    deleting {0} {1} audit logs".format(model_cls.history.using(using).all().count(), model_cls._meta.object_name)
        model_cls.history.using(using).all().delete()

    def reset_model_raw_sql(self, model_cls):
        from django.db import connections, transaction
        cursor = connections[self.get_using_destination()].cursor()
        table_name = format(model_cls._meta.db_table)
        raw_sql_query = "DELETE FROM `{0}`".format(table_name)
        cursor.execute(raw_sql_query)
        transaction.commit_unless_managed(using=self.get_using_destination())
        print " deleted"

    def delete_audit_instances_raw_sql(self, model_cls):
        from django.db import connections, transaction
        cursor = connections[self.get_using_destination()].cursor()
        print "    deleting {0} audit logs".format(model_cls.history.using(self.get_using_destination()).all().count())
        audit_table_name = "{0}_audit".format(model_cls._meta.db_table)
        raw_sql_query = "DELETE FROM `{0}`".format(audit_table_name)
        cursor.execute(raw_sql_query)
        transaction.commit_unless_managed(using=self.get_using_destination())
        print " deleted"

    def reset_listed_models(self, models):
        for app_name, model_name in models:
            model_cls = get_model(app_name, model_name)
            self.reset_model(model_cls)

    def update_model(self, model_or_app_model_tuple, additional_base_model_class=None):
        try:
            app, model = model_or_app_model_tuple
            model_cls = get_model(app, model)
        except:
            model_cls = model_or_app_model_tuple
        #additional_base_model_class = model_cls
        self.model_to_json(model_cls, additional_base_model_class)

    def reset_app_models(self, app_name):
        print '    deleting for app {0}...'.format(app_name)
        for model_cls in get_models(get_app(app_name)):
            self.reset_model(model_cls)
