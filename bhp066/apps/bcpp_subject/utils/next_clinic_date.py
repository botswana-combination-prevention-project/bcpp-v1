from datetime import datetime
from dateutil.relativedelta import relativedelta


def next_clinic_date(community_clinic_days, base_datetime=None, allow_same_day=None):
    """Returns next clinic date that is not today or None.

    community_clinic_days format is a ClinicDaysTuple. See bcpp_household.mappers for format.

    """
    clinic_dates = []
    base_datetime = base_datetime or datetime.today()
    for DAY in community_clinic_days.days:
        if allow_same_day:
            clinic_dates.append(base_datetime + relativedelta(weekday=DAY(+1)))
        elif base_datetime + relativedelta(weekday=DAY(+1)) != base_datetime:
            clinic_dates.append(base_datetime + relativedelta(weekday=DAY(+1)))
    next_clinic_datetime = datetime(min(clinic_dates).year, min(clinic_dates).month, min(clinic_dates).day, 7, 30, 0)
    return next_clinic_datetime
