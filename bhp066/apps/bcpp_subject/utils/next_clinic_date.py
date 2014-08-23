from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django.conf import settings


def next_clinic_date(community_code, clinic, today=None, community_clinic_days=None, referral_code=None):
    """Returns next clinic date that is not today or None."""
    next_clinic_datetime = None
    clinic_dates = []
    today = today or date.today()
    community_clinic_days = community_clinic_days or settings.CLINIC_DAYS
    DAYS = community_clinic_days.get(community_code).get(clinic)
    if DAYS:
        for DAY in DAYS[0]:
            if today + relativedelta(weekday=DAY(+1)) != today:
                clinic_dates.append(today + relativedelta(weekday=DAY(+1)))
        next_clinic_datetime = datetime(min(clinic_dates).year, min(clinic_dates).month, min(clinic_dates).day, 7, 30, 0)
    return next_clinic_datetime
