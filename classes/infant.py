from datetime import datetime
from django.forms import ValidationError
from django.db.models import get_model
from bhp_identifier.models import SubjectIdentifier, DerivedSubjectIdentifier


class Infant(object):
    
    """ Create subject identifier(s) for an infant(s) by calling get_identifier() with the maternal identifier and return a dictionary {infant order: identifier}. """
    
    def __init__(self):
        pass

    def consent_required(self):
        return False
    
    def get_identifier(self, user, **kwargs):

        """ Return identifier or a tuple of identifiers (if twins).
        
            * Information comes from a delivery form usually, not a consent. 
            * Names, initials, gender and DOB are not expected to be known yet.
            * Subject Identifier is derived from the maternal identifier so the SubjectIdentifier model is not updated. 
            
            """
            
        # maternal identifier should exist in SubjectIdentifier
        maternal_identifier=kwargs.get('maternal_identifier')
        if not SubjectIdentifier.objects.filter(subject_identifier=maternal_identifier):
            raise ValidationError('Unknown maternal_identifier {0}.'.format(maternal_identifier))
        # differentiate between live and live to register 
        # as mother may not wish to include all in study
        maternal_study_site=kwargs.get('maternal_study_site')
        subject_type=kwargs.get('subject_type')
        live_infants=kwargs.get('live_infants')
        live_infants_to_register=kwargs.get('live_infants_to_register')
        # some checks on logic of live and live to register 
        if live_infants_to_register==0:
            raise ValidationError("Number of live_infants_to_register may not be 0!.")
        if live_infants_to_register>live_infants:
            raise ValidationError("Number of infants to register may not exceed number of live infants.")
        # get a starting suffix based on number of live_infants
        suffix=self._get_base_suffix(live_infants)
        subject_identifier={}      
        for infant_order in range(0, live_infants_to_register):
            # if more than one infant, increment suffix by 10's
            suffix+=(infant_order) * 10
            # infant identifier is the maternal identifier plus a suffix
            subject_identifier.update({infant_order:"{maternal_identifier}-{suffix}".format(maternal_identifier=maternal_identifier, suffix=suffix)})           
            # save to  DerivedSubjectIdentifier model which enforces uniqueness
            DerivedSubjectIdentifier.objects.create(subject_identifier = subject_identifier.get(infant_order), 
                                                    base_identifier = maternal_identifier)
        self._register_infants(user, maternal_identifier, maternal_study_site, subject_type, live_infants, live_infants_to_register)
        #return a dictionary { infant order: identifier }    
        return subject_identifier
            
    def _register_infants(self, user, maternal_identifier, maternal_study_site, subject_type, live_infants, live_infants_to_register):
        
        """ Identify and Register infant(s) and associate with the mother's subject_identifier and study site. 
        
            Infant identifier is the maternal identifier plus a suffix """
        
        RegisteredSubject=get_model('bhp_registration', 'registeredsubject')
        # get a starting suffix based on live_infants
        suffix = self._get_base_suffix(live_infants)
        identifier = []
        # loop through range of live_infants_to_register and register
        for infant_order in range(0, live_infants_to_register):
            # if more than one infant, increment suffix by 10's
            suffix += (infant_order) * 10
            # infant identifier is the maternal identifier plus a suffix
            identifier.append("{maternal_identifier}-{suffix}".format(maternal_identifier=maternal_identifier, suffix=suffix))           
            # create new record in RegisteredSubject
            # Names, initials, gender and DOB are not expected to be known yet
            RegisteredSubject.objects.create(    
                subject_identifier = identifier[infant_order],
                registration_datetime = datetime.now(),
                subject_type = 'infant', 
                user_created = user,
                created = datetime.now(),
                first_name = '',
                initials = '',
                registration_status = 'registered',
                relative_identifier = maternal_identifier, 
                study_site = maternal_study_site,       
                )
        if len(identifier) == 1:
            return identifier[0]
        else:
            return identifier    
        
    def _get_base_suffix(self, live_infants):
        
        """ Return a two digit suffix based on the number of live infants. 
        
            In the case of twins, triplets, ... will be incremented by 10's during registration for each subsequent infant registered. """
        
        if live_infants == 1:
            suffix = 10 # singlet 10
        elif live_infants == 2:
            suffix = 25 # twins 25,26
        elif live_infants == 3:
            suffix = 36 # triplets 36,37,38
        elif live_infants == 4:
            suffix = 47 # quadruplets 47,48,49,50
        else:
            raise TypeError('Ensure number of infants is greater than 0 and less than or equal to 4. You wrote %s' % (live_infants))
        return suffix
        