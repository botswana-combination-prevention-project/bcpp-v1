from django.db.models import get_model
from bhp_identifier.classes import SubjectIdentifier
#from bhp_registration.models import RegisteredSubject


class ConsentedSubjectIdentifier(SubjectIdentifier):
    """ Manages identifiers for subject consents.

    Note, registered subject is created on a signal in bhp_subject by the consent model (which is a subclass of BaseSubject)."""

    def __init__(self, site_code, using=None):
        super(ConsentedSubjectIdentifier, self).__init__(site_code=site_code, using=using)

# removed, see signal in bhp_subject
#     def get_identifier_post(self, new_identifier, **kwargs):
#         """ Updates registered subject after a new subject identifier is created."""
#         # the model, for creating a new instance
#         RegisteredSubject = get_model('bhp_registration', 'registeredsubject')
#         # access registered subject manager method
#         consent = kwargs.get('consent')
#         attrname = kwargs.get('consent_attrname')
#         setattr(consent, attrname, new_identifier)
#         RegisteredSubject.objects.update_with(consent, attrname, **kwargs)
#         return new_identifier
