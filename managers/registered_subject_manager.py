from datetime import datetime
from django.db import models
from django.db.models import Count
from bhp_variables.models import StudySpecific
from bhp_registration.models import SubjectIdentifierAuditTrail


class RegisteredSubjectManager(models.Manager):
    
    """Manager class for RegisteredSubject model."""
    
    def register_subject(self, consent_model, subject_type='SUBJECT', user='', **kwargs):
        
        """
        Register a subject by allocating an identifier at the time of consent and storing in model RegisteredSubject.
        
        Generate an identifier and save it back to the consent form 
        and update the identifier audit trail.
        
        The consent_model is the selected and new consent. Count=1
            
        """
        
        #if kwargs.get('registered_subject'):
        #    raise TypeError()
        
        subject_identifier = {}
        
        #get the consent just created
        #consent = SubjectConsent.objects.get(pk=new_pk)

        subject_identifier['site'] = consent_model.study_site.site_code
        
        #add a new record in the audit trail for this consent and identifier-'to be'
        #leave subject_identifier 'null' for now
        audit = SubjectIdentifierAuditTrail(
            subject_consent_id=consent_model.pk, 
            first_name = consent_model.first_name,
            initials = consent_model.initials,
            date_allocated=datetime.now(),
            user_created = user,
            )
         
        # saving here will cause integrity error if from a proxy model    
        #audit.save()    

        # get the auto-increment id for the new audit trail record
        # just created above
        # subject_identifier['audit_id'] = audit.pk

        # prepare the subject identifier by 
        # getting the seed and prefix and deviceid, modulus
        settings = StudySpecific.objects.all()
        subject_identifier['modulus'] = settings.subject_identifier_modulus
        subject_identifier['seed'] = settings.subject_identifier_seed
        subject_identifier['prefix']= settings.subject_identifier_prefix
        
        subject_identifier['device_id'] = kwargs.get('device_id', None)

             
        if not subject_identifier['device_id']:
            subject_identifier['device_id'] = settings.device_id          
        
        if subject_identifier['device_id'] == '98':
            raise TypeError("Subject_identifier_device_id cannot be \'%s\'. Configure bhp_variables.StudySpecific or set hostname to end in a 2 digit number?", (subject_identifier['device_id'],))
        # get subject identifier sequence, is count of subject_type +1
        subject_identifier['seq'] = 1
        if super(RegisteredSubjectManager,self).filter(subject_type__iexact = subject_type):
            agg = super(RegisteredSubjectManager,self).filter(subject_type__iexact = subject_type).aggregate(Count('subject_identifier'))
            subject_identifier['seq'] += agg['subject_identifier__count']

        # using the seed, device and audit trail id determine the integer segment of the id 
        # subject_identifier['int'] = (((subject_identifier['seed'] * subject_identifier['device_id']) + subject_identifier['seq'])) 
        # changed this, i want the device ID to appear in the number. the above would 
        # not result in this. For example (seed*device_id)+seq  (10000*98)+4024 = 102024
        # TODO: allow device_id to be an alpha numeric ?? or 3 digits might be better...
        subject_identifier['int'] = int(str(subject_identifier['device_id'])+str(subject_identifier['seq']))


        # using the integer segment, calculate the check digit
        check_digit = subject_identifier['int'] % subject_identifier['modulus']

        # pad the check digit if required based on the modulus
        if subject_identifier['modulus'] > 100 and subject_identifier['modulus'] <= 1000:
            if check_digit <10:
                subject_identifier['check_digit'] = "00%s" % (check_digit)
            if check_digit >=10 and check_digit < 100:
                subject_identifier['check_digit'] = "%0s" % (check_digit)    
            if check_digit >=100 and check_digit < 1000:
                subject_identifier['check_digit'] = "%s" % (check_digit)                

        if subject_identifier['modulus'] > 10 and subject_identifier['modulus'] <= 100:
            if check_digit <10:
                subject_identifier['check_digit'] = "0%s" % (check_digit)
            if check_digit >=10 and check_digit < 100:
                subject_identifier['check_digit'] = "%s" % (check_digit)    
        
        if subject_identifier['modulus'] <= 10:
            subject_identifier['check_digit'] = "%s" % (check_digit) 

        #create the formatted identifier
        subject_identifier['identifier'] = "%s-%s%s-%s" % (subject_identifier['prefix'], subject_identifier['site'],subject_identifier['int'],  subject_identifier['check_digit'] )

        # update subject_identifier to the audit trail table
        # unless registered subject was passed in kwargs
        # if registered_subject was passed implies the 
        # subject is being re-consented or re-registered. 
        audit.subject_identifier = subject_identifier['identifier']
        if 'registered_subject' not in kwargs:
            audit.save()
            if super(RegisteredSubjectManager,self).filter(subject_identifier__exact = subject_identifier['identifier']):
                raise TypeError("RegisteredSubjectManager attempted to generate non-unique subject identifier subject type '%s'. Got '%s'" % (subject_type, subject_identifier['identifier']))
            
        # you may pass the RegisteredSubject object and update instead of creating a new one
        # pass when calling this manager (for example, from save_model in admin)
        if 'registered_subject' in kwargs:
            registered_subject =  kwargs['registered_subject']               
            registered_subject.subject_consent_id = consent_model.pk
            registered_subject.subject_identifier = subject_identifier['identifier']
            registered_subject.first_name = consent_model.first_name
            registered_subject.study_site = consent_model.study_site
            registered_subject.may_store_samples = consent_model.may_store_samples
            registered_subject.initials = consent_model.initials
            registered_subject.gender = consent_model.gender
            registered_subject.subject_type = subject_type
            registered_subject.registration_datetime = datetime.now()
            registered_subject.registration_status = 'consented'
            registered_subject.identity = consent_model.identity
            registered_subject.dob = consent_model.dob
            registered_subject.is_dob_estimated = consent_model.is_dob_estimated
            registered_subject.save()
        else:        
            super(RegisteredSubjectManager, self).create(
                    created = datetime.now(),
                    user_created = user,
                    subject_consent_id = consent_model.pk,
                    subject_identifier = subject_identifier['identifier'],
                    first_name = consent_model.first_name,
                    study_site = consent_model.study_site,
                    may_store_samples = consent_model.may_store_samples,
                    initials = consent_model.initials,
                    gender = consent_model.gender,
                    subject_type = subject_type,
                    registration_datetime = datetime.now(),
                    registration_status = 'consented',
                    identity = consent_model.identity,
                    dob = consent_model.dob,
                    is_dob_estimated = consent_model.is_dob_estimated,
                )
                
        # return the new subject identifier to the form currently being save()'d
        return subject_identifier['identifier']

    def register_live_infants(self, ** kwargs):

        """
        Allocate infant identifiers for as many live_infants_to_register.
        
        Choose an id_suffix based on the value of live_infants. So if 
        live_infants <> live_infants_to_register, use live_infants to
        determine the suffix, and live_infants_to_register for the number
        to register
        
        """

        registration_model = kwargs.get('registration_model')
        registered_mother = kwargs.get('mother_identifier')
        live_infants = kwargs.get('live_infants')
        live_infants_to_register = kwargs.get('live_infants_to_register')
        user = kwargs.get('user')

        if live_infants_to_register == 0:
            raise TypeError("Number of live_infants_to_register cannot be 0! Test for this in admin before calling register_live_infants().")
        
        if live_infants_to_register > live_infants:
            # Trap this on the form, not here!!
            raise TypeError("Number of infants to register may not exceed number of live infants.")
        
        subject_identifier = {}

        subject_identifier['mother'] = registered_mother.subject_identifier   
        
        # we use the mother's consent as the consent pk to store in 
        # registered subject for this/these infant(s)

        first_name=''
        initials=''
        id_suffix = 0

        if live_infants == 1:
            id_suffix = 10
        elif live_infants == 2:
            id_suffix = 25
        elif live_infants == 3:
            id_suffix = 36
        elif live_infants == 4:
            id_suffix = 47
        else:
            raise TypeError('Ensure number of infants is greater than 0 and less than or equal to 4. You wrote %s' % (live_infants))

        for infant_order in range(0, live_infants_to_register):
            id_suffix += (infant_order) * 10
            subject_identifier['id'] = "%s-%s" % (subject_identifier['mother'], id_suffix)            
            super(RegisteredSubjectManager, self).create(    
                subject_identifier = subject_identifier['id'],
                registration_datetime = datetime.now(),
                subject_type = 'infant', 
                user_created = user,
                created = datetime.now(),
                #subject_consent_id=kwargs.get('consent_pk'),
                first_name = first_name,
                initials = initials.upper(),
                registration_status = 'registered',
                relative_identifier = registered_mother.subject_identifier, 
                study_site = registered_mother.study_site,       
                )                

        # update subject_identifier to the audit trail table
        # audit.subject_identifier = subject_identifier['identifier']
        # audit.save()
        return True
