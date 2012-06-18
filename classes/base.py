from django.db.models import get_model
from django.core.exceptions import ImproperlyConfigured
#from bhp_consent.classes import ConsentDescriptor


class Base(object):
    
    #consent = ConsentDescriptor()

    def __init__(self, *args, **kwargs):
        # the model, for creating a new instance
        self.RegisteredSubject = get_model('bhp_registration', 'registeredsubject')
        # the instance, if set, will be updated instead of creating a new instance
        self.registered_subject = None
        # need an instance of the consent, raise an error later if not available
        self.consent = None
        # set by get_identifier
        self.subject_identifier = None
        
    def _consent_required(self):
        return True
    
    def get_identifier(self, subject_type, site, **kwargs):
        raise ImproperlyConfigured('Method \'assign_identifier\' must be overridden by the subclass for {0}'.format(self.name))
    
    def update_register(self, consent, attrname='subject_identifier', **kwargs):
        """ update for this subject in registered subject """
        # access registered subject manager method
        self.RegisteredSubject.objects.update_with(consent, attrname, **kwargs)