from datetime import date, timedelta
from django.core.exceptions import ValidationError
from bhp_variables.models import StudySpecific


def MinConsentAge (value):
    now  = date.today()
    ss = StudySpecific.objects.all()[0]
    
    min_consent_age_years = ss.minimum_age_of_consent
    min_consent_age_days = 365*min_consent_age_years
    age_in_days = timedelta(days=min_consent_age_days)
    if value > now - age_in_days:
        raise ValidationError(u'Participant must be %syrs or older. Date of birth suggests otherwise. You entered %s ' % (min_consent_age_years, value))

def MaxConsentAge (value):
    now  = date.today()
    ss = StudySpecific.objects.all()[0]
    max_consent_age_years = ss.maximum_age_of_consent
    max_consent_age_days = 365*max_consent_age_years
    age_in_days = timedelta(days=max_consent_age_days)
    if value < now - age_in_days:
        raise ValidationError(u'Participant must be no older than %syrs. Date of birth suggests otherwise. You entered %s ' % (max_consent_age_years, value))

