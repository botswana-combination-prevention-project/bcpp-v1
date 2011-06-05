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

@register.filter(name='admin_url_for_maternal_dashboard')
def admin_url_for_maternal_dashboard(contenttype, maternal_visit_pk):
    """Return a url to add or change an admin entry form via the maternal dashboard based on maternal_visit_pk"""
    if contenttype.model_class().objects.filter(maternal_visit = maternal_visit_pk):
        model = contenttype.model_class().objects.get(maternal_visit = maternal_visit_pk)
        view = 'admin:%s_%s_change' % (contenttype.app_label, contenttype.model)
        view = str(view)
        rev_url = reverse(view, args=(model.pk,))
        rev_url = '%s?%s' % (rev_url, 'next=maternal_dashboard_visit_url&dashboard=maternal')            
        #else:
        #    raise TypeError("Maternal_visit_pk is not None but does not exist for model '%s'. Got '%s'" % (contenttype.model, maternal_visit_pk))
    else:
        view = 'admin:%s_%s_add' % (contenttype.app_label, contenttype.model)
        view = str(view)
        try:
            rev_url = reverse(view)
            rev_url = '%s?maternal_visit=%s&%s' % (rev_url, maternal_visit_pk, 'next=maternal_dashboard_visit_url&dashboard=maternal')            
        except:
            raise TypeError('NoReverseMatch while rendering reverse for %s_%s in admin_url_from_contenttype. Is model registered in admin?' % (contenttype.app_label, contenttype.model))    
    return rev_url

    
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



