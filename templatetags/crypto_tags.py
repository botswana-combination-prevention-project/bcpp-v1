from django import template
from bhp_crypto.classes import Crypter

register = template.Library()

@register.filter(name='encrypted')
def encrypted(value):
    retval = value  
    crypter = Crypter()
    if isinstance(value, basestring):
        retval = crypter.mask_encrypted(value)
    return retval 
