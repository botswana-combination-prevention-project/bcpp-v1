from django.forms import ValidationError
from bhp_identifier.models import SubjectIdentifier
from base_subject_identifier import BaseSubjectIdentifier


class PartnerIdentifier(BaseSubjectIdentifier):

    """ Create the subject identifier for a partner by calling get_identifier() with the index subject identifier. """

    def get_identifier_prep(self, **kwargs):
        """Prepares to create an identifier consisting of the the index identifier and a -10 suffix."""
        options = {}
        subject_identifier = kwargs.get('subject_identifier')
        if not SubjectIdentifier.objects.filter(identifier=subject_identifier):
            raise ValidationError('Unknown subject_identifier {0}.'.format(subject_identifier))
        options.update(
            app_name='bhp_identifier',
            models_name='derived_subject_identifier',
            subject_identifier=kwargs.get('subject_identifier'),
            user=kwargs.get('user'),
            suffix='10',
            identifier_format="{subject_identifier}-{suffix}",
            subject_type='partner')
        return options
