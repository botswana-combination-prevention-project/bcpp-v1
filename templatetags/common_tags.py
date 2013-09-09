import subprocess
import os
import re
import socket
from math import ceil
from datetime import date
from django import template
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from bhp_common.utils import formatted_age, convert_from_camel

register = template.Library()


@register.simple_tag
def hostname():
    return socket.gethostname()


@register.simple_tag
def current_time(format_string):
    return date.today().strftime(format_string)


@register.simple_tag
def project_title():
    if 'PROJECT_TITLE' not in dir(settings):
        raise ImproperlyConfigured('Attribute settings.PROJECT_TITLE not found. Please add PROJECT_TITLE=\'<long name of my project>\' to the settings file.')
    return settings.PROJECT_TITLE


@register.simple_tag
def project_number():
    if 'PROJECT_NUMBER' not in dir(settings):
        raise ImproperlyConfigured('Attribute settings.PROJECT_NUMBER not found. Please add PROJECT_NUMBER=\'<project number, e.g. BHP041>\' to the settings file.')
    return settings.PROJECT_NUMBER


@register.simple_tag
def app_name():
    if 'APP_NAME' not in dir(settings):
        raise ImproperlyConfigured('Attribute settings.APP_NAME not found. Please add APP_NAME=\'<short name of my project>\' to the settings file.')
    return settings.APP_NAME


@register.simple_tag
def protocol_revision():
    if 'PROTOCOL_REVISION' not in dir(settings):
        raise ImproperlyConfigured('Attribute settings.PROTOCOL_REVISION not found. Please add PROTOCOL_REVISION=\'<document version and date>\' to the settings file.')
    return settings.PROTOCOL_REVISION


@register.simple_tag
def institution():
    if 'INSTITUTION' not in dir(settings):
        raise ImproperlyConfigured('Attribute settings.INSTITUTION not found. Please add INSTITUTION=\'<institution name>\' to the settings file.')
    return settings.INSTITUTION


@register.simple_tag
def get_model_name(model):
    return model._meta.module_name


@register.simple_tag
def get_app_label(model):
    return model._meta.app_label


@register.filter(name='model_verbose_name')
def model_verbose_name(contenttype):
    return contenttype.model_class()._meta.verbose_name


@register.filter(name='add_nbsp')
def add_nbsp(value):
    if value:
        return value.replace(' ', '&nbsp;')
    return ''


@register.filter(name='mask_pk')
def mask(value, mask):
    return '<{0}>'.format(mask)


@register.filter(name='subject_identifier')
def subject_identifier(value, mask=None):
    retval = ''
    if value:
        pattern = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        if not 'subject_identifier' in dir(value):
            retval = ''
        elif pattern.match(value.subject_identifier):
            retval = '{0}'.format(mask or 'subject_identifier not set')
        else:
            retval = value.subject_identifier
    return retval


@register.filter(name='admin_url_from_contenttype')
def admin_url_from_contenttype(contenttype):
    view = 'admin:%s_%s_add' % (contenttype.app_label, contenttype.model)
    view = str(view)
    try:
        rev_url = reverse(view)
    except:
        raise TypeError('NoReverseMatch while rendering reverse for %s_%s in admin_url_from_contenttype. Is model registered in admin?' % (contenttype.app_label, contenttype.model))
    return rev_url


@register.filter(name='user_full_name')
def user_full_name(username):
    if not username:
        return ''
    else:
        try:
            user = User.objects.get(username__iexact=username)
            return '%s %s (%s)' % (user.first_name, user.last_name, user.get_profile().initials)
        except:
            return username


@register.filter(name='user_initials')
def user_initials(username):
    if not username:
        return ''
    else:
        try:
            user = User.objects.get(username__iexact=username)
            return user.get_profile().initials
        except:
            return username


@register.filter(name='age')
def age(born):
    reference_date = date.today()
    return formatted_age(born, reference_date)


@register.filter(name='dob_or_dob_estimated')
def dob_or_dob_estimated(dob, is_dob_estimated):
    if dob > date.today():
        return 'Unknown'
    elif is_dob_estimated.lower() == '-':
        return dob.strftime('%Y-%m-%d')
    elif is_dob_estimated.lower() == 'd':
        return dob.strftime('%Y-%m-XX')
    elif is_dob_estimated.lower() == 'md':
        return dob.strftime('%Y-XX-XX')
    else:
        return dob.strftime('%Y-%m-%d')


@register.filter(name='get_item')
def get_item(items, key):
    if isinstance(items, dict):
        return items.get(key, None)
    if isinstance(items, (list, tuple)):
        try:
            return items[key]
        except:
            pass
    return None


@register.filter(name='get_revision')
def get_revision(opts):
    """Returns the svn revision number for the model\'s file using Opts (_meta)."""
    try:
        rev = subprocess.check_output(
            ['svn', 'info', '{0}.py'.format(convert_from_camel(opts.object_name))],
            cwd=os.path.join(settings.DIRNAME, '/'.join([opts.app_label, 'models/']))
            )
        #s = re.search('Revision: [0-9]+', rev)
        s = re.search('Last Changed Rev: [0-9]+', rev)
        return s.group().split(': ')[1]
    except:
        pass
    return '?'


@register.filter(name='get_field')
def get_field(obj, field_attr=None):
    try:
        return getattr(obj, field_attr)
    except:
        pass
    return None


@register.filter(name='get_meta')
def get_meta(obj):
    try:
        return obj._meta
    except:
        pass
    return None


@register.filter(name='get_verbose_name')
def get_verbose_name(obj):
    return obj._meta.verbose_name


@register.filter(name='gender')
def gender(value):
    if value.lower() == 'f':
        return 'Female'
    elif value.lower() == 'm':
        return 'Male'
    elif value.lower() == '-1':
        return '?'
    elif value.lower() == '-9':
        return '?'
    else:
        return value


@register.filter(name='roundup')
def roundup(num, places):
    if isinstance(num, (int, float)):
        fl = float(num)
        return ceil(fl * (10 ** places)) / (10 ** places)
    else:
        return num


@register.filter
def divide_by(x, y):
    if x == 0 or y == 0:
        return 0
    else:
        return x / y
