import re
from datetime import datetime, date, timedelta
from django.core.exceptions import ValidationError
from bhp_variables.models import StudySpecific

def BWCellNumber(value):
    str_value = "%s" % (value)
    p = re.compile('^[7]{1}[123456]{1}[0-9]{6}$')
    if p.match(str_value):
        raise ValidationError(u'Invalid cell number. You entered %s.' % value)
    
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

def dob_gt_eq_18 (value):
    now  = date.today()
    d18 = 365*18
    age_in_days = timedelta(days=d18)
    if value > now - age_in_days:
        raise ValidationError(u'Participant must be 18yrs or older. Date of birth suggests otherwise. You entered %s ' % (value))

def dob_gt_eq_16 (value):
    age_in_years=64
    now  = date.today()
    day_years = 365*age_in_years
    age_in_days = timedelta(days=day_years)
    if value >= now - age_in_days:
        raise ValidationError(u'Participant must be %syrs or older. Date of birth suggests otherwise. You entered %s ' % (age_in_years, value))

def dob_lt_eq_64 (value):
    age_in_years=64
    now  = date.today()
    day_years = 365*age_in_years
    age_in_days = timedelta(days=day_years)
    if value <= now - age_in_days:
        raise ValidationError(u'Participant must be %syrs or younger. Date of birth suggests otherwise. You entered %s ' % (age_in_years, value))

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
    started  = dte.study_start_datetime
    protocol_number = dte.protocol_number
    if value < started:
        raise ValidationError(u'Date cannot be before the study started. %s started on %s. You entered %s.' % (protocol_number, started, value,))

def datetime_not_before_study_start (value):
    dte = StudySpecific.objects.all()[0]
    started  = dte.study_start_datetime
    protocol_number = dte.protocol_number
    if value < started:
        raise ValidationError(u'Date and time cannot be before the study started. %s started on %s. You entered %s.' % (protocol_number, started, value,))

def eligible_if_yes (value):        
    if value != 'Yes':
        raise ValidationError('If No, Participant is NOT ELIGIBLE and registration cannot continue.')
        
def eligible_if_no (value):        
    if value != 'No':
        raise ValidationError('If Yes, Participant is NOT ELIGIBLE and registration cannot continue.')        
        
def eligible_if_female (value):        
    if value != 'F':
        raise ValidationError('If gender not Female, Participant is NOT ELIGIBLE and registration cannot continue.')

def eligible_if_male (value):        
    if value != 'M':
        raise ValidationError('If gender not Male, Participant is NOT ELIGIBLE and registration cannot continue.')
        
def eligible_if_negative (value):        
    if value != 'NEG':
        raise ValidationError('Participant must be HIV Negative. Participant is NOT ELIGIBLE and registration cannot continue.')
        
