from django.db.models import get_model
from bhp_registration.models import RegisteredSubject
from bhp_identifier.classes import SubjectIdentifier


class ConsentedSubjectIdentifier(SubjectIdentifier):

    def get_identifier_post(self, consent, attrname, **kwargs):
        """ Updates registered subject after a new subject identifier is created."""
        # the model, for creating a new instance
        RegisteredSubject = get_model('bhp_registration', 'registeredsubject')
        # access registered subject manager method
        RegisteredSubject.objects.update_with(consent, attrname, **kwargs)
