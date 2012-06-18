from datetime import datetime
#from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from bhp_registration.models import SubjectIdentifierAuditTrail
from bhp_crypto.managers import CryptoManager
from bhp_identifier.classes import Subject, Infant, Partner


class RegisteredSubjectManager(CryptoManager):
    
    def update_with(self, instance, attrname='subject_identifier', **kwargs):
        """ Use an instance, usually a consent, to update registered subject.
        Assume all required fields attributes are included in the instance"""
        valid_attrnames = ('subject_identifier', 'pk')
        if attrname not in valid_attrnames:
            raise TypeError('Attribute must represent a unique field such as {0}. Got {1}.'.format(', '.join(valid_attrnames), attrname))
        #if found update, otherwise raise an error
        if super(RegisteredSubjectManager,self).filter(**{attrname:getattr(instance,attrname)}):
            registered_subject = super(RegisteredSubjectManager,self).get(**{attrname:getattr(instance,attrname)})
            registered_subject.registration_datetime = datetime.today()
            registered_subject.modified = datetime.today()
            registered_subject.first_name = instance.first_name
            registered_subject.initials = instance.initials
            registered_subject.gender = instance.gender
            registered_subject.study_site = instance.study_site
            registered_subject.identity = instance.identity
            registered_subject.dob = instance.dob
            registered_subject.is_dob_estimated = instance.is_dob_estimated
            registered_subject.may_store_samples = instance.may_store_samples
            registered_subject.subject_type = instance.get_subject_type()
            # set values for any additional attributes, or overwrite the value from above
            for attr in kwargs:
                if kwargs.get(attr):
                    setattr(registered_subject, attr, kwargs.get(attr)) 
            registered_subject.save()
        else:
            #raise ObjectDoesNotExist('Expected Registered Subject but not found for %s' % (getattr(instance, attrname),))
            super(RegisteredSubjectManager,self).create(
                relative_identifier = kwargs.get('relative_identifier', None),
                subject_identifier = kwargs.get('subject_identifier'),
                registration_datetime = datetime.today(),
                created = datetime.today(),
                first_name = instance.first_name,
                initials = instance.initials,
                gender = instance.gender,
                study_site = instance.study_site,
                identity = instance.identity,
                dob = instance.dob,
                is_dob_estimated = instance.is_dob_estimated,
                may_store_samples = instance.may_store_samples,
                subject_type = instance.get_subject_type(),
                )
                
    #    def register_subject(self, consent, subject_type='SUBJECT', user='', **kwargs):
    #        
    #        """
    #        Register a subject by allocating an identifier at the time of consent and storing in model 
    #        RegisteredSubject.
    #        
    #        Generate an identifier and save it back to the consent form 
    #        and update the identifier audit trail.            
    #        """
    #        
    #        #does this subject already exist in registered_subject? If so, just return the subject_identifier
    #        #check for same identity and firstname and dob
    #        if super(RegisteredSubjectManager,self).filter(identity=consent.identity):
    #            return super(RegisteredSubjectManager,self).get(identity=consent.identity).subject_identifier
    #        #check for same firstname, initials and dob
    #        elif super(RegisteredSubjectManager,self).filter(first_name = consent.first_name,
    #                                                        dob = consent.dob,
    #                                                        initials = consent.initials):
    #            return super(RegisteredSubjectManager,self).get(
    #                                                            first_name = consent.first_name,
    #                                                            dob = consent.dob,
    #                                                            initials = consent.initials,
    #                                                            ).subject_identifier
    #        # did you pass registered_subject as a keyword argument, with the subject_identifier?
    #        elif 'registered_subject' in kwargs:
    #            if kwargs.get('registered_subject').subject_identifier:
    #                return kwargs.get('registered_subject').subject_identifier
    #        else:
    #            pass
    #        
    #        #add a new record in the audit trail for this consent and identifier-'to be'
    #        audit = SubjectIdentifierAuditTrail(
    #            subject_consent_id=consent.pk, 
    #            date_allocated=datetime.now(),
    #            user_created = user,
    #            )
    #
    #        # get a new subject_identifier
    #        subject = Subject()
    #        subject_identifier = subject.get_identifier(subject_type = subject_type,
    #                                                    site = consent.study_site.site_code,
    #                                                    registration_status = 'consented')
    #        
    #        # update subject_identifier to the audit trail table
    #        # unless registered subject was passed in kwargs
    #        # if registered_subject was passed implies the 
    #        # subject is being re-consented or re-registered. 
    #        audit.subject_identifier = subject_identifier
    #        if 'registered_subject' not in kwargs:
    #            audit.save()
    #            if super(RegisteredSubjectManager,self).filter(subject_identifier__exact = subject_identifier):
    #                raise TypeError("RegisteredSubjectManager attempted to generate non-unique subject identifier subject type '%s'. Got '%s'" % (subject_type, subject_identifier))
    #            
    #        # you may pass the RegisteredSubject object and update instead of creating a new one
    #        # pass when calling this manager (for example, from save_model in admin)
    #        if 'registered_subject' in kwargs:
    #            registered_subject =  kwargs.get('registered_subject')            
    #            registered_subject.subject_consent_id = consent.pk
    #            registered_subject.subject_identifier = subject_identifier
    #            registered_subject.first_name = consent.first_name
    #            registered_subject.study_site = consent.study_site
    #            registered_subject.may_store_samples = consent.may_store_samples
    #            registered_subject.initials = consent.initials
    #            registered_subject.gender = consent.gender
    #            registered_subject.subject_type = subject_type
    #            registered_subject.registration_datetime = datetime.now()
    #            registered_subject.registration_status = 'consented'
    #            registered_subject.identity = consent.identity
    #            registered_subject.dob = consent.dob
    #            registered_subject.is_dob_estimated = consent.is_dob_estimated
    #            registered_subject.save()
    #        else:        
    #            super(RegisteredSubjectManager, self).create(
    #                    created = datetime.now(),
    #                    user_created = user,
    #                    subject_consent_id = consent.pk,
    #                    subject_identifier = subject_identifier,
    #                    first_name = consent.first_name,
    #                    study_site = consent.study_site,
    #                    may_store_samples = consent.may_store_samples,
    #                    initials = consent.initials,
    #                    gender = consent.gender,
    #                    subject_type = subject_type,
    #                    registration_datetime = datetime.now(),
    #                    registration_status = 'consented',
    #                    identity = consent.identity,
    #                    dob = consent.dob,
    #                    is_dob_estimated = consent.is_dob_estimated,
    #                )
    #                
    #        # return the new subject identifier to the form currently being save()'d
    #        return subject_identifier

    def register_live_infants(self, ** kwargs):

        """ Identify and register the number of live infants "to register" and return identifier(s). """
        maternal_identifier = kwargs.get('maternal_identifier').subject_identifier
        maternal_site = kwargs.get('maternal_site').subject_identifier
        live_infants = kwargs.get('live_infants')
        live_infants_to_register = kwargs.get('live_infants_to_register')
        user = kwargs.get('user')
        infant = Infant()
        subject_identifier = infant.get_identifier(user, 
                              maternal_identifier = maternal_identifier,
                              maternal_site = maternal_site,
                              live_infants = live_infants,
                              live_infants_to_register = live_infants_to_register,)
        return subject_identifier
    
    def register_partner(self, ** kwargs):
        """ Allocate partner identifiers. """
        index_identifier = kwargs.get('index_identifier')
        first_name = kwargs.get('partner_first_name')
        initials = kwargs.get('partner_initials')
        site = kwargs.get('study_site')
        user = kwargs.get('user')
        partner = Partner()        
        subject_identifier = partner.get_identifier(user, 
                               index_identifier = index_identifier, 
                               first_name = first_name,
                               initials = initials,
                               site = site,)        
                 

        return subject_identifier
    
