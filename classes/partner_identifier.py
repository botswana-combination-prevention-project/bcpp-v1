from datetime import datetime
from django.db.models import get_model
from django.forms import ValidationError
from bhp_identifier.models import SubjectIdentifier, DerivedSubjectIdentifier


class PartnerIdentifier(object):

    """ Create the subject identifier for a partner by calling get_identifier() with the index subject identifier. """

    def __init__(self):
        pass

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
#    
#    def get_identifier(self, index_identifier, subject_type, **kwargs):
#        """ Just add a -10 to the index identifier and register.
#        *Probably not creating the identifier because of a consent
#        *Subject Identifier is derived from the index identifier so the
#        SubjectIdentifier model is referenced but not updated.""" 
#        # index_identifier identifier should exist in SubjectIdentifier
#        
#        #..todo: TODO: for maikalelo, this needs to be updated
#        # STOP!!
#        raise TypeError('You may not overrise get_identifier.')
#        consent=None
#        
#        
#        if not SubjectIdentifier.objects.filter(subject_identifier=index_identifier):
#            raise ValidationError('Unknown index_identifier {0}.'.format(index_identifier))
#        subject_identifier = "{}-10",format(index_identifier)
#        # create/save to DerivedSubjectIdentifier
#        DerivedSubjectIdentifier.objects.create(subject_identifier=subject_identifier, 
#                                                base_identifier=index_identifier)        
#        RegisteredSubject = get_model('bhp_registration', 'registeredsubject')
#        if not RegisteredSubject.objects.filter(relative_identifier = index_identifier):
#            RegisteredSubject.objects.update_with(consent, )
#            RegisteredSubject.objects.create(    
#                relative_identifier = index_identifier, 
#                subject_identifier = subject_identifier,
#                registration_datetime = datetime.now(),
#                subject_type = subject_type, 
#                user_created = consent.user,
#                created = datetime.now(),
#                first_name = consent.first_name,
#                initials = consent.initials.upper(),
#                registration_status = 'not_contacted',
#                study_site = consent.study_site,       
#                )
#        else:
#            ValidationError('A partner has already been registered for index {}'.format(index_identifier))
