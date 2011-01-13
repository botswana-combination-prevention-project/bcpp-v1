from datetime import datetime, date, timedelta
from django.core.exceptions import ValidationError
from bhp_study_variables.models import Configuration

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

def date_not_before_study_start (value):
    dte = Configuration.objects.all()[0]
    started  = dte.study_start_datetime
    protocol_number = dte.protocol_number
    if value < started:
        raise ValidationError(u'Date cannot be before the study started. %s started on %s. You entered %s.' % (protocol_number, started, value,))

def datetime_not_before_study_start (value):
    dte = Configuration.objects.all()[0]
    started  = dte.study_start_datetime
    protocol_number = dte.protocol_number
    if value < started:
        raise ValidationError(u'Date and time cannot be before the study started. %s started on %s. You entered %s.' % (protocol_number, started, value,))
