from datetime import date, timedelta, datetime
from bhp_registration.models import SubjectIdentifierAuditTrail
from bhp_variables.models import StudySpecific
from models import RegisteredSubject, RandomizedSubject

def AllocateIdentifier(consent_model, subject_type='SUBJECT', user=''):
    
    """
    Allocate an identifier at the time of consent
    
    generate an identifier and save it back to the consent form 
    and update the identifier audit trail.
    
    consent_model is the selected and new consent. Count=1
        
    """
    
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
        
    audit.save()    


    # get the auto-increment id for the new audit trail record
    # just created above
    subject_identifier['audit_id'] = audit.pk

    # prepare the subject identifier by 
    # getting the seed and prefix and deviceid, modulus
    settings = StudySpecific.objects.all()[0]
    subject_identifier['modulus'] = settings.subject_identifier_modulus
    subject_identifier['seed'] = settings.subject_identifier_seed
    subject_identifier['prefix']= settings.subject_identifier_prefix
    subject_identifier['device_id']= settings.device_id
    
    # using the seed, device and audit trail id determine the integer segment of the id 
    subject_identifier['int'] = (((subject_identifier['seed']* subject_identifier['device_id']) + subject_identifier['audit_id'])) 

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
    audit.subject_identifier = subject_identifier['identifier']
    audit.save()
    
    RegisterSubject(
        identifier=subject_identifier['identifier'], 
        consent_pk=consent_model.pk, 
        first_name=consent_model.first_name, 
        initials=consent_model.initials, 
        subject_type=subject_type, 
        user=user)
    
    # return the new subject identifier to the form currently being save()'d
    return subject_identifier['identifier']
    
def AllocateInfantIdentifier(** kwargs):

    registration_model = kwargs.get('registration_model')
    registered_mother = kwargs.get('mother_identifier')
    live_infants = kwargs.get('live_infants')
    user = kwargs.get('user')
   
    """
    Allocate an identifier at the time of consent
    
    generate a mother identifier and save it back to the consent form 
    and update the identifier audit trail.
    
    registration_model is for example, mp005 (delivery form), or the 
    form that has the live_infants field
    
        
    """
    
    subject_identifier = {}
    

    #rm = RegisteredSubject.objects.get(subject_identifier__exact=registered_mother.subject_identifier)
    subject_identifier['mother'] = registered_mother.subject_identifier   
    
    #add a new record in the audit trail for this consent and identifier-'to be'

    #audit = SubjectIdentifierAuditTrail(
    #    subject_consent_id=consent, 
    #    first_name = consent.first_name,
    #    initials = consent.initials,
    #    date_allocated=datetime.now(),
    #    user_created = user,
    #    )

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

    
    for infant_order in range(0, live_infants):
        id_suffix += (infant_order) * 10
        subject_identifier['id'] = "%s-%s" % (subject_identifier['mother'], id_suffix)            
        RegisterSubject(
            identifier = subject_identifier['id'], 
            relative_identifier = registered_mother.subject_identifier,
            consent_pk = registered_mother.pk, 
            first_name = first_name, 
            initials = initials, 
            subject_type = 'infant', 
            user = user)

    # update subject_identifier to the audit trail table
    # audit.subject_identifier = subject_identifier['identifier']
    # audit.save()
    
    return True

def RegisterSubject (**kwargs):

    if kwargs.get('identifier') is None:
        raise TypeError( 'bhp_registration.RegisterSubject expects a value for \'identifier\'. Got None.')

    if kwargs.get('consent_pk') is None:
        raise TypeError( 'bhp_registration.RegisterSubject expects a value for \'consent_pk\'. Got None.')

    if kwargs.get('first_name') is None:
        raise TypeError( 'bhp_registration.RegisterSubject expects a value for \'first_name\'. Got None.')
        
    if kwargs.get('initials') is None:
        raise TypeError( 'bhp_registration.RegisterSubject expects a value for \'initials\'. Got None.')

    if kwargs.get('subject_type') is None:
        raise TypeError( 'bhp_registration.RegisterSubject expects a value for \'subject_type\'. Got None.')
    
    if kwargs.get('user') is None:
        raise TypeError( 'bhp_registration.RegisterSubject expects a value for \'user\'. Got None.')

    
    registered_subject = RegisteredSubject(    
        subject_identifier = kwargs.get('identifier'),
        registration_datetime=datetime.now(),
        subject_type = kwargs.get('subject_type').upper(),
        user_created=kwargs.get('user'),
        created=datetime.now(),
        subject_consent_id=kwargs.get('consent_pk'),
        first_name=kwargs.get('first_name'),
        initials=kwargs.get('initials').upper(),
        registration_status='registered',
        relative_identifier = kwargs.get('relative_identifier'),        
        )
    
    registered_subject.save()
    
    return registered_subject    

"""
    A Randmized subject must always be Registered first
    
"""    
def RandomizeSubject (consent_model, subject_type, user):
    
    #try:
    #consent = SubjectConsent.objects.get(pk=subject_consent) 
    
    dte=datetime.now()
    
    ObjRS = RegisteredSubject.objects.get(subject_identifier=consent_model.subject_identifier) 
    ObjRS.randomization_datetime=dte
    ObjRS.registration_status='randomized'
    ObjRS.save()
    
    objRandS = RandomizedSubject(    
        subject_identifier = consent_model.subject_identifier,
        registration_datetime=dte,
        randomization_datetime=dte,
        subject_type = subject_type,
        user_created=user,
        created=datetime.now(),
        subject_consent_id=consent_model.pk,
        first_name=consent_model.first_name,
        initials=consent_model.initials,
        )
    
    objRandS.save()
    
    return objRandS
    
