from edc.utils import split_seq

from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU


def split_weekdays(days, base_datetime):
    """Returns a list of day objects in reversed order.

    For example: given a start day of WED the reverse of
    [MO, TH FR] is [MO, FR TH] in that from WED the previous
    day is MO, then FRI, then TH working backwards.
    """
    wk = [MO, TU, WE, TH, FR, SA, SU]
    weekdays = [day.weekday for day in days]
    weekdays.append(base_datetime.weekday())
    weekdays.sort()
    for item in [x for x in split_seq(weekdays, base_datetime.weekday())]:
        item.reverse()
        for i in item:
            reversed.append(i)
    return [wk[i] for i in reversed]
