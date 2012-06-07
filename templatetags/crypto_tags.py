from django import template
from bhp_crypto.classes import Crypter

register = template.Library()

@register.filter(name='encrypted')
def encrypted(value):
    crypter = Crypter()
    if crypter.is_encrypted(value):
        ret_val = '<encrypted>'
    else:
        ret_val = value    
    return ret_val 
