from django.db.models import get_model
from bhp_identifier.classes import SubjectIdentifier


class ConsentedSubjectIdentifier(SubjectIdentifier):

    def get_identifier_post(self, new_identifier, **kwargs):
        """ Updates registered subject after a new subject identifier is created."""
        # the model, for creating a new instance
        RegisteredSubject = get_model('bhp_registration', 'registeredsubject')
        # access registered subject manager method
        consent = kwargs.get('consent')
        attrname = kwargs.get('consent_attrname')
        setattr(consent, attrname, new_identifier)
        RegisteredSubject.objects.update_with(consent, attrname, **kwargs)
        return new_identifier
