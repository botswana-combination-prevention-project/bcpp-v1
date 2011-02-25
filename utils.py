from datetime import date, timedelta, datetime
from bhp_consent.models import SubjectIdentifierAuditTrail
from bhp_variables.models import StudySpecific
from models import RegisteredSubject, RandomizedSubject

def AllocateIdentifier(ObjConsent, subject_type='SUBJECT', user=''):
    
    """
    Allocate an identifier at the time of consent
    
    generate an identifier and save it back to the consent form 
    and update the identifier audit trail.
    
    ObjConsent is the selected and new consent. Count=1
        
    """
    
    subject_identifier = {}
    
    #get the consent just created
    #consent = SubjectConsent.objects.get(pk=new_pk)

    subject_identifier['site'] = ObjConsent.study_site.site_code
    
    #add a new record in the audit trail for this consent and identifier-'to be'
    #leave subject_identifier 'null' for now
    audit = SubjectIdentifierAuditTrail(
        subject_consent_id=ObjConsent.pk, 
        first_name = ObjConsent.first_name,
        initials = ObjConsent.initials,
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
    
    RegisterSubject (subject_identifier['identifier'], ObjConsent.pk, ObjConsent.first_name, ObjConsent.initials, subject_type, user)
    
    # return the new subject identifier to the form currently being save()'d
    return subject_identifier['identifier']
    
def AllocateInfantIdentifier(ObjParentForm, registered_mother, live_infants, user):
    
    """
    Allocate an identifier at the time of consent
    
    generate a mother identifier and save it back to the consent form 
    and update the identifier audit trail.
    
    ObjParentForm is for example, mp005 (delivery form), or the 
    form that has the live_infants field
    
        
    """
    
    subject_identifier = {}
    
    #get the consent just created
    #consent = SubjectConsent.objects.get(pk=new_pk)


    rm = RegisteredSubject.objects.get(subject_consent_id=registered_mother)

    subject_identifier['mother'] = rm.subject_identifier
    
    #add a new record in the audit trail for this consent and identifier-'to be'
    #leave subject_identifier 'null' for now
    #audit = SubjectIdentifierAuditTrail(
    #    subject_consent_id=consent, 
    #    first_name = consent.first_name,
    #    initials = consent.initials,
    #    date_allocated=datetime.now(),
    #    user_created = user,
    #    )
    #audit.save()

    # get the number of live births from mp005
    #if live_infants == 1:

    # we use the mother's consent as the consent pk to store in 
    # registered subject for this/these infant(s)
    first_name=''
    initials=''
    if live_infants == 1:
        subject_identifier['id'] = "%s-%s" % (subject_identifier['mother'], '10')
        ret = RegisterSubject(subject_identifier['id'], registered_mother, first_name, initials, 'infant', user)
    if live_infants == 2:
        subject_identifier['id'] = "%s-%s" % (subject_identifier['mother'], '25')
        ret = RegisterSubject(subject_identifier['id'], registered_mother, first_name, initials, 'infant', user)
        subject_identifier['id'] = "%s-%s" % (subject_identifier['mother'], '35')
        ret = RegisterSubject(subject_identifier['id'], registered_mother, first_name, initials, 'infant', user)
    if live_infants == 3:
        subject_identifier['id'] = "%s-%s" % (subject_identifier['mother'], '47')
        ret = RegisterSubject(subject_identifier['id'], registered_mother, first_name, initials, 'infant', user)
        subject_identifier['id'] = "%s-%s" % (subject_identifier['mother'], '57')
        ret = RegisterSubject(subject_identifier['id'], registered_mother, first_name, initials, 'infant', user)
        subject_identifier['id'] = "%s-%s" % (subject_identifier['mother'], '67')
        ret = RegisterSubject(subject_identifier['id'], registered_mother, first_name, initials, 'infant', user)
    if live_infants == 4:
        subject_identifier['id'] = "%s-%s" % (subject_identifier['mother'], '48')
        ret = RegisterSubject(subject_identifier['id'], registered_mother, first_name, initials, 'infant', user)
        subject_identifier['id'] = "%s-%s" % (subject_identifier['mother'], '58')
        ret = RegisterSubject(subject_identifier['id'], registered_mother, first_name, initials, 'infant', user)
        subject_identifier['id'] = "%s-%s" % (subject_identifier['mother'], '68')
        ret = RegisterSubject(subject_identifier['id'], registered_mother, first_name, initials, 'infant', user)
        subject_identifier['id'] = "%s-%s" % (subject_identifier['mother'], '78')
        ret = RegisterSubject(
                    subject_identifier['id'], 
                    registered_mother, 
                    first_name, 
                    initials, 
                    'infant', 
                    user)
           


    # update subject_identifier to the audit trail table
    # audit.subject_identifier = subject_identifier['identifier']
    # audit.save()
    
    # return the new subject identifier to the form currently being save()'d
    return True

def RegisterSubject (identifier, consent_pk, first_name, initials, subject_type, user):
    
    #try:
    #consent = SubjectConsent.objects.get(pk=subject_consent) 
    subject_type=subject_type.upper()
    
    ObjRS = RegisteredSubject(    
        subject_identifier = identifier,
        registration_datetime=datetime.now(),
        subject_type = subject_type,
        user_created=user,
        created=datetime.now(),
        subject_consent_id=consent_pk,
        first_name=first_name,
        initials=initials,
        registration_status='registered',
        )
    
    ObjRS.save()
    
    return ObjRS    

"""
    A Randmized subject must always be Registered first
    
"""    
def RandomizeSubject (ObjConsent, subject_type, user):
    
    #try:
    #consent = SubjectConsent.objects.get(pk=subject_consent) 
    
    dte=datetime.now()
    
    ObjRS = RegisteredSubject.objects.get(subject_identifier=ObjConsent.subject_identifier) 
    ObjRS.randomization_datetime=dte
    ObjRS.registration_status='randomized'
    ObjRS.save()
    
    objRandS = RandomizedSubject(    
        subject_identifier = ObjConsent.subject_identifier,
        registration_datetime=dte,
        randomization_datetime=dte,
        subject_type = subject_type,
        user_created=user,
        created=datetime.now(),
        subject_consent_id=ObjConsent.pk,
        first_name=ObjConsent.first_name,
        initials=ObjConsent.initials,
        )
    
    objRandS.save()
    
    return objRandS
    
