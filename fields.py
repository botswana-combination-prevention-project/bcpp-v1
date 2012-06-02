"""
Erik's additional encrypted model fields, try one!
"""
from django.db import models
#from django.db.models import CharField
from classes import BaseEncryptedField
#from django_extensions.db.fields.encrypted import EncryptedCharField


class EncryptedIdentityField(BaseEncryptedField):
    __metaclass__ = models.SubfieldBase
    
    def get_internal_type(self):
        return "TextField"

    #def formfield(self, **kwargs):
    #    defaults = {'max_length': 1024}        
    #    defaults.update(kwargs)
    #    return super(EncryptedIdentityField, self).formfield(**defaults)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)