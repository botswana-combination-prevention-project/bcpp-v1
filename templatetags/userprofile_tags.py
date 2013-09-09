from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter(name='salutation')
def salutation(username):
    if not username:
        return ''
    else:    
        try:
            if User.objects.get(username__iexact=username).get_profile().salutation == 'NONE':
                return ''
            else:     
                return '%s. ' % User.objects.get(username__iexact=username).get_profile().salutation
        except:
            return ''
