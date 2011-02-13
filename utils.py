from datetime import date, timedelta, datetime
from bhp_consent.models import SubjectIdentifierAuditTrail
from bhp_variables.models import StudySpecific
from models import RegisteredSubject, RandomizedSubject

def AllocateIdentifier(ObjConsent, user):
    
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
    subject_identifier['int'] = ((subject_identifier['seed'] + subject_identifier['audit_id']) * 100) + subject_identifier['device_id']
    
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
    
    # return the new subject identifier to the form currently being save()'d
    return subject_identifier['identifier']
    


def RegisterSubject (ObjConsent, subject_type, user):
    
    #try:
    #consent = SubjectConsent.objects.get(pk=subject_consent) 
    
    ObjRS = RegisteredSubject(    
        subject_identifier = ObjConsent.subject_identifier,
        registration_datetime=datetime.now(),
        subject_type = subject_type,
        user_created=user,
        created=datetime.now(),
        subject_consent_id=ObjConsent.pk,
        first_name=ObjConsent.first_name,
        initials=ObjConsent.initials,
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
    
