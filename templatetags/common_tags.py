from datetime import *
from dateutil.relativedelta import *
from django import template
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from bhp_common.utils import formatted_age, round_up

register = template.Library()

@register.filter(name='model_verbose_name')
def model_verbose_name(contenttype):
    return contenttype.model_class()._meta.verbose_name
    
@register.filter(name='admin_url_from_contenttype')
def admin_url_from_contenttype(contenttype, object_id=''):
    if contenttype.model_class().objects.filter(pk=object_id):
        view = 'admin:%s_%s_change' % (contenttype.app_label, contenttype.model)
        view = str(view)
        return reverse(view, args=(object_id,))
    else:
        view = 'admin:%s_%s_add' % (contenttype.app_label, contenttype.model)
        view = str(view)
        return reverse(view)
    
@register.filter(name='user_full_name')
def user_full_name(username):
    if not username:
        return ''
    else:    
        try:
            user=User.objects.get(username__iexact=username)
            return '%s %s (%s)' % (user.first_name, user.last_name, user.get_profile().initials)
        except:
            return username

@register.filter(name='user_initials')
def user_initials(username):
    if not username:
        return ''
    else:    
        try:
            user=User.objects.get(username__iexact=username)
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
def roundup(d, digits):
    return round_up(d, digits)   



