from datetime import datetime
from dateutil.relativedelta import relativedelta, MO, TU, WE

from django.conf import settings

clinic_days = {
    '11': MO,
    '12': MO,
    '13': TU,
    '14': MO,
    '15': MO,
    '16': MO,
    '17': MO,
    '18': MO,
    '19': MO,
    '20': MO,
    '21': MO,
    '22': MO,
    '23': MO,
    '24': MO,
    '25': MO,
    '26': MO,
    '27': MO,
    '28': MO,
    '29': MO,
    '30': MO,
    '31': MO,
    '32': MO,
    '33': MO,
    '34': MO,
    '35': MO,
    '36': MO,
    '37': MO,
    '38': MO,
    '39': MO,
    '40': MO,
    }


def next_clinic_date():
    D = clinic_days.get(settings.SITE_CODE)
    return datetime.today() + relativedelta(D(+1))
