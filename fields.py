"""
Erik's additional model fields
"""

import sys, socket
from django.db.models import CharField
from django_extensions.db.fields import UUIDField
#from django_extensions.db.fields.encrypted import EncryptedCharField


class MyUUIDField (UUIDField):
    """
    http://code.djangoproject.com/ticket/12235
    subclassed to avoid MultiValueDictKeyError when editing Inline objects
    """
    def contribute_to_class(self, cls, name):
        if self.primary_key == True: 
            assert not cls._meta.has_auto_field, "A model can't have more than one AutoField: %s %s %s; have %s" % (self,cls,name,cls._meta.auto_field)
            super(MyUUIDField, self).contribute_to_class(cls, name)
            cls._meta.has_auto_field = True
            cls._meta.auto_field = self
        else:
            super(MyUUIDField, self).contribute_to_class(cls, name)

class HostnameCreationField (CharField):  
    """ 
    HostnameCreationField

    By default, sets editable=False, blank=True, default=socket.gethostname()
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('max_length', 50)
        kwargs.setdefault('verbose_name', 'Hostname')
        kwargs.setdefault('default', socket.gethostname())
        CharField.__init__(self, *args, **kwargs)


    def get_internal_type(self):
        return "CharField"
  
    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)

class HostnameModificationField (CharField):  
    """ 
    HostnameModificationField

    By default, sets editable=False, blank=True, default=socket.gethostname()
    
    Sets value to socket.gethostname() on each save of the model.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('max_length', 50)
        kwargs.setdefault('verbose_name', 'Hostname')
        kwargs.setdefault('default', socket.gethostname())
        CharField.__init__(self, *args, **kwargs)

    def pre_save(self, model, add):
        value = socket.gethostname()
        setattr(model, self.attname, value)
        return value

    def get_internal_type(self):
        return "CharField"
  
    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
        
class OtherCharField(CharField):
    """field for "Other specify" options"""
            
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', True)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('max_length', 35)
        kwargs.setdefault('verbose_name', '...if "Other", specify')
        CharField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "CharField"
  
    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
        
class DobField(DateTimeField):
    """field for date of birth"""
            
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', True)
        kwargs.setdefault('help_text', 'Format is YYYY-MM-DD)
        DateTimeField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "DateTimeField"
  
    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.DateTimeField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)

class WeightField(DecimalField):
    """field for weight"""
            
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', True)
        kwargs.setdefault('max_digits', 5)
        kwargs.setdefault('max_places', 1)                        
        kwargs.setdefault('help_text', 'Format is 999.9 in Kg)
        DecimalField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "DecimalField"
  
    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.DecimalField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)

class OmangField(CharField):
    """field for omang"""
           
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', True)
        kwargs.setdefault('max_length', 9)
        kwargs.setdefault('help_text', 'Format is 9999[12]9999)
        CharField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "CharField"
  
    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)

#class MyEncryptedCharField(EncryptedCharField):        
#    
#    def get_db_prep_value(self, value):
#        #if not value.startswith(self.prefix):
#        #    value = self.prefix + self.crypt.Encrypt(value)
#        return value
        

