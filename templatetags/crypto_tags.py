from django import template
from bhp_crypto.utils import mask_encrypted

register = template.Library()


@register.filter(name='encrypted')
def encrypted(value):
    retval = value
    if isinstance(value, basestring):
        retval = mask_encrypted(value)
    return retval
