from datetime import datetime, date, timedelta
import re
from django.core.exceptions import ValidationError
from bhp_variables.models import StudySpecific
from bhp_variables.choices import GENDER_OF_CONSENT


def MinDecimalValidator(value, min_value):
    if min_value > value :
        raise ValidationError(u'Ensure this value is greater than or equal to %s.' % value)
            
def MaxDecimalValidator(value, max_value):
    if max_value < value :
        raise ValidationError(u'Ensure this value is less than or equal to %s.' % value)
            
def TelephoneNumber(value, pattern, word):
    str_value = "%s" % (value)
    p = re.compile(pattern)
    if p.match(str_value) == None:
        raise ValidationError(u'Invalid %s number. You entered %s.' % (word, str_value))

def BWCellNumber(value):
    TelephoneNumber(value, '^[7]{1}[123456]{1}[0-9]{6}$', 'cell')
    
def BWTelephoneNumber(value):
    TelephoneNumber(value, '^[2-8]{1}[0-9]{6}$', 'telephone')

def IsTodayDateTime (value):
    pass
    
def dob_not_future (value):
    now  = date.today()
    if now < value :
        raise ValidationError(u'Date of birth cannot be a future date. You entered %s.' % value)

def dob_not_today (value):
    now  = date.today()
    if now == value :
        raise ValidationError(u'Date of birth cannot be today. You entered %s.' % value)

def datetime_not_future (value):
    now  = datetime.now()
    time_error = timedelta(minutes=10)
    if value > datetime.now() + time_error:
        raise ValidationError(u'Date cannot be a future date and time. You entered %s' % (value,))

def date_not_future (value):
    now  = date.today()
    if value > now:
        raise ValidationError(u'Date cannot be a future date. You entered %s' % (value,))

def datetime_is_future (value):
    now  = datetime.now()
    time_error = timedelta(minutes=10)
    if value < datetime.now() + time_error:
        raise ValidationError(u'Date must be a future date and time. You entered %s' % (value,))

def date_is_future (value):
    now  = date.today()
    if value < now:
        raise ValidationError(u'Date must be a future date. You entered %s' % (value,))

def date_not_future (value):
    now  = date.today()
    if value > now:
        raise ValidationError(u'Date must not be a future date. You entered %s' % (value,))

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


def GenderOfConsent (value):
    ss = StudySpecific.objects.all()[0]
    
    gender_allowed = ss.gender_of_consent
    
    if gender_allowed == 'MF':
        allowed = ('MF', 'Male and Female')
        entry = ('value', value)
    else:
        for lst in GENDER_OF_CONSENT:
            if lst[0] == gender_allowed:
                allowed = lst
   
        for lst in GENDER_OF_CONSENT:
            if lst[0] == value:
                entry = lst
        
    if value != allowed[0] and allowed[0] != 'MF':    
        raise ValidationError(u'Gender of consent is %s. You entered %s.' % ( allowed[1], entry[1]))


def datetime_is_future (value):
    now  = datetime.today()
    if value < now:
        raise ValidationError(u'Date and time must be a future date and time. You entered %s' % (value,))

def datetime_is_after_consent (value):
    """ not working..."""
    now  = value
    if value != now:
        raise ValidationError(u'Date and time cannot be prior to consent date. You entered %s' % (value,))

def date_not_before_study_start (value):
    dte = StudySpecific.objects.all()[0]
    value_datetime = datetime(value.year, value.month, value.day, 0,0)
    started  = dte.study_start_datetime
    protocol_number = dte.protocol_number
    if value_datetime < started:
        raise ValidationError(u'Date cannot be before the study started. %s started on %s. You entered %s.' % (protocol_number, started, value,))

def datetime_not_before_study_start (value):
    dte = StudySpecific.objects.all()[0]
    started  = dte.study_start_datetime
    protocol_number = dte.protocol_number
    if value < started:
        raise ValidationError(u'Date and time cannot be before the study started. %s started on %s. You entered %s.' % (protocol_number, started, value,))

def eligible_if_yes (value):        
    if value != 'Yes':
        raise ValidationError('Participant is NOT ELIGIBLE. Registration cannot continue.')
        
def eligible_if_no (value):        
    if value != 'No':
        raise ValidationError('Participant is NOT ELIGIBLE. Registration cannot continue.')
          
def eligible_if_unknown (value):        
    if value != 'Unknown':
        raise ValidationError('Participant is NOT ELIGIBLE. Registration cannot continue.')              
        
def eligible_if_female (value):        
    if value != 'F':
        raise ValidationError('If gender not Female, Participant is NOT ELIGIBLE and registration cannot continue.')

def eligible_if_male (value):        
    if value != 'M':
        raise ValidationError('If gender not Male, Participant is NOT ELIGIBLE and registration cannot continue.')
        
def eligible_if_negative (value):        
    if value != 'NEG':
        raise ValidationError('Participant must be HIV Negative. Participant is NOT ELIGIBLE and registration cannot continue.')

def Omang(value):
    """ note this can also be checked at the form level"""
    check_omang_field(value)
    
            
        
