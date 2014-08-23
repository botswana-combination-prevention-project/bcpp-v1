from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django.conf import settings


def next_clinic_date(community_code, clinic, base_datetime=None, community_clinic_days=None, allow_same_day=None):
    """Returns next clinic date that is not today or None.

    community_clinic_days format is {<clinic_type>': ((weekday, weekday, ...), <start_date or None>), ...}

        {'IDCC': ((MO, WE), ),
         'ANC': ((MO, TU, WE, TH, FR), ),
         'SMC': ((MO, TU, WE, TH, FR), date(2014, 10, 15)),
         'SMC-ECC': ((MO, TU, WE, TH, FR), date(2014, 10, 7))}

    """
    next_clinic_datetime = None
    clinic_dates = []
    base_datetime = base_datetime or datetime.today()
    community_clinic_days = community_clinic_days or settings.CLINIC_DAYS.get(community_code)
    DAYS = community_clinic_days.get(clinic)
    if DAYS:
        for DAY in DAYS[0]:
            if allow_same_day:
                clinic_dates.append(base_datetime + relativedelta(weekday=DAY(+1)))
            elif base_datetime + relativedelta(weekday=DAY(+1)) != base_datetime:
                clinic_dates.append(base_datetime + relativedelta(weekday=DAY(+1)))
        next_clinic_datetime = datetime(min(clinic_dates).year, min(clinic_dates).month, min(clinic_dates).day, 7, 30, 0)
    return next_clinic_datetime
