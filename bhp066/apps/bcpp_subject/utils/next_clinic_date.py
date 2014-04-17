from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta, MO, TU, WE  # , TH, FR

from django.conf import settings

clinic_days = {
    '11': (MO, WE),
    '12': (MO, WE),
    '13': (TU, WE),
    '14': (MO, WE),
    '15': (MO, WE),
    '16': (MO, WE),
    '17': (MO, WE),
    '18': (MO, WE),
    '19': (MO, WE),
    '20': (MO, WE),
    '21': (MO, WE),
    '22': (MO, WE),
    '23': (MO, WE),
    '24': (MO, WE),
    '25': (MO, WE),
    '26': (MO, WE),
    '27': (MO, WE),
    '28': (MO, WE),
    '29': (MO, WE),
    '30': (MO, WE),
    '31': (MO, WE),
    '32': (MO, WE),
    '33': (MO, WE),
    '34': (MO, WE),
    '35': (MO, WE),
    '36': (MO, WE),
    '37': (MO, WE),
    '38': (MO, WE),
    '39': (MO, WE),
    '40': (MO, WE),
    }


def next_clinic_date():
    """Returns next clinic date that is not today."""
    TODAY = date.today()
    for D in clinic_days.get(settings.SITE_CODE):
        clinic_date = date.today() + relativedelta(weekday=D(+1))
        if relativedelta(TODAY, clinic_date).days > 0:
            break
    return datetime(clinic_date.year, clinic_date.month, clinic_date.day, 7, 30, 0)
