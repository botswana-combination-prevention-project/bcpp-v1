from datetime import date, datetime, timedelta
from django.core.exceptions import ValidationError
from bhp_variables.models import StudySpecific


def IsTodayDateTime (value):
    pass
    
def datetime_not_future (value):
    time_error = timedelta(minutes=10)
    if value > datetime.now() + time_error:
        raise ValidationError(u'Date cannot be a future date and time. You entered %s' % (value,))

def date_not_future (value):
    now  = date.today()
    if value > now:
        raise ValidationError(u'Date cannot be a future date. You entered %s' % (value,))

def datetime_is_future (value):
    time_error = timedelta(minutes=10)
    if value < datetime.now() + time_error:
        raise ValidationError(u'Date must be a future date and time. You entered %s' % (value,))

def date_is_future (value):
    now  = date.today()
    if value < now:
        raise ValidationError(u'Date must be a future date. You entered %s' % (value,))
    
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
