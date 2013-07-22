import socket
from django_extensions.db.fields import UUIDField
from django.db.models import CharField
from django.utils.translation import ugettext as _


class MyUUIDField (UUIDField):
    """
    http://code.djangoproject.com/ticket/12235
    subclassed to avoid MultiValueDictKeyError when editing Inline objects
    """
    description = _("Custom Uuid field")

    def contribute_to_class(self, cls, name):
        if self.primary_key == True:
            assert not cls._meta.has_auto_field, "A model can't have more than one AutoField: %s %s %s; have %s" % (self, cls, name, cls._meta.auto_field)
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

    description = _("Custom field for hostname created")

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
    description = _("Custom field for hostname modified")

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
