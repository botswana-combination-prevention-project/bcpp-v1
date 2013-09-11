from __future__ import print_function
from django.db import models
from django.conf import settings
from django.contrib import admin
from bhp_common.utils import convert_from_camel
from bhp_crypto.fields import EncryptedTextField, EncryptedIntegerField, EncryptedDecimalField, EncryptedCharField, EncryptedAesCharField, EncryptedFirstnameField, EncryptedLastnameField, EncryptedOtherCharField, EncryptedIdentityField
from bhp_visit_tracking.models import BaseVisitTracking


admin.autodiscover()


def create_factory_files(app_label, factory_path=None):
    """Creates factory files in the tests/factories folder in the specified app.

    Loops through admin registry to find all registered models and inlines. A factory
    will not be created for models not registered in admin.

    Use within shell_plus::
        from bhp_factory.utils.gen_factories import *

        create_factory_files('bcpp_htc_subject')
    """
    if not factory_path:
        factory_path = '{0}/{1}/tests/factories'.format(settings.DIRNAME, app_label)
    for model, model_admin in admin.site._registry.iteritems():
        if app_label == model._meta.app_label:
            if model_admin.inlines:
                for inline_admin in model_admin.inlines:
                    model_name = inline_admin.model._meta.object_name
                    print('{0}_{1}_add'.format(inline_admin.model._meta.app_label, model_name.lower()))
                    fname = '{0}/{1}_factory.py'.format(factory_path, convert_from_camel(model_name))
                    _create_file(fname, inline_admin.model)
            model_name = model._meta.object_name
            print('{0}_{1}_add'.format(model._meta.app_label, model_name.lower()))
            fname = '{0}/{1}_factory.py'.format(factory_path, convert_from_camel(model_name))
            _create_file(fname, model)


def create_factory_init(app_label):
    import_stmt = []
    for model, model_admin in admin.site._registry.iteritems():
        if app_label == model._meta.app_label:
            if model_admin.inlines:
                for inline_admin in model_admin.inlines:
                    import_stmt.append('from {0}_factory import {1}Factory'.format(convert_from_camel(inline_admin.model._meta.object_name), inline_admin.model._meta.object_name))
            import_stmt.append('from {0}_factory import {1}Factory'.format(convert_from_camel(model._meta.object_name), model._meta.object_name))
    print('\n'.join(import_stmt))


def _add_field_to_factory(field):
    add = ''
    add_field = ''
    add_import = ''
    if not field.null == True and field.name not in ['id', 'subject_visit', 'user_created', 'user_modified', 'created', 'modified', 'hostname_created', 'hostname_modified']:
        if isinstance(field, (models.DecimalField, EncryptedDecimalField)):
            add = '2.5'
        elif isinstance(field, (models.IntegerField, EncryptedIntegerField)):
            add = '2'
        elif isinstance(field, (models.FloatField, )):
            add = '2.1234567'
        elif isinstance(field, (models.CharField, models.TextField, EncryptedTextField, EncryptedCharField, EncryptedAesCharField, EncryptedFirstnameField, EncryptedLastnameField, EncryptedOtherCharField, EncryptedIdentityField)):
            if field.choices:
                add = '{0}[0][0]'.format(field.choices)
            else:
                add = 'factory.Sequence(lambda n: \'{0}{{0}}\'.format(n))'.format(field.name)
        elif isinstance(field, models.IntegerField):
            add = '1'
        elif isinstance(field, models.TimeField):
            add = 'datetime.today().strftime(\'%H:%m\')'
        elif isinstance(field, (models.DateField, models.DateTimeField)):
            if 'DateTime' in type(field).__name__:
                add = 'datetime.today()'
            else:
                add = 'date.today()'
        elif isinstance(field, (models.ForeignKey, models.OneToOneField)):
            add_import = 'from {0}.tests.factories import {1}Factory'.format(field.rel.to._meta.app_label, field.rel.to.__name__)
            add = 'factory.SubFactory({0}Factory)'.format(field.rel.to.__name__)
        elif isinstance(field, models.BooleanField):
            add = 'True'
        else:
            raise TypeError('{0}'.format(field.__class__))
        add_field = '    {0} = {1}'.format(field.name, add)
    return (add_field, add_import)


def _create_file_for_uuid_model(fname, model_admin):
    app_label = model_admin._meta.app_label
    model_name = model_admin._meta.object_name
    import_content = ('import factory\n'
             'from datetime import date, datetime\n'
             'from bhp_base_model.tests.factories import BaseUuidModelFactory\n'
             'from {app_label}.models import {model_name}').format(app_label=app_label, model_name=model_name)
    class_content = ('\n\nclass {model_name}Factory(BaseUuidModelFactory):\n'
             '    FACTORY_FOR = {model_name}').format(app_label=app_label, model_name=model_name)
    return import_content, class_content


def _create_file_for_scheduled_model(fname, model_admin):
    app_label = model_admin._meta.app_label
    model_name = model_admin._meta.object_name
    import_content = ('import factory\n'
             'from datetime import date, datetime\n'
             'from {app_label}.tests.factories import SubjectVisitFactory\n'
             'from base_scheduled_model_factory import BaseScheduledModelFactory\n'
             'from {app_label}.models import {model_name}').format(app_label=app_label, model_name=model_name)
    class_content = ('\n\nclass {model_name}Factory(BaseScheduledModelFactory):\n'
             '    FACTORY_FOR = {model_name}\n\n'
             '    subject_visit = factory.SubFactory(SubjectVisitFactory)').format(app_label=app_label, model_name=model_name)
    return import_content, class_content


def _create_file(fname, model_admin, uuid=False, scheduled=False):
    app_label = model_admin._meta.app_label
    model_name = model_admin._meta.object_name
    if not uuid and not scheduled:
        for field in models.get_model(app_label, model_name)._meta.fields:
            if isinstance(field, BaseVisitTracking):
                scheduled = True
                break
        if not scheduled:
            uuid = True
    if uuid:
        import_content, class_content = _create_file_for_uuid_model(fname, model_admin)
    elif scheduled:
        import_content, class_content = _create_file_for_scheduled_model(fname, model_admin)
    else:
        raise
    field_content = ''
    for field in model_admin._meta.fields:
        add_content = _add_field_to_factory(field)
        if add_content[0]:
            field_content = '{0}\n{1}'.format(field_content, add_content[0])
        if add_content[1]:
            import_content = '{0}\n{1}'.format(import_content, add_content[1])
    f = file(fname, "w+")
    print(import_content, file=f)
    print(class_content, file=f)
    if field_content:
        print(field_content, file=f)
    f.close
