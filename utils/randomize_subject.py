from datetime import date, timedelta, datetime
from bhp_registration.models import SubjectIdentifierAuditTrail
from bhp_variables.models import StudySpecific
from bhp_registration.models import RegisteredSubject

"""
    A Randmized subject must always be Registered first

"""

'''
def RandomizeSubject (consent_model, subject_type, user):

    #try:
    #consent = SubjectConsent.objects.get(pk=subject_consent) 

    dte = datetime.now()

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
    
'''