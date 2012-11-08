

def get_upper_range_days(age_upper_range_value, age_upper_range_unit, operator):
    """Converts the upper range value into days considering the operator.

    .. note:: If the operator is <= then the unit (M,Y) then ((range_value + 1) * number of days per unit) - 1) is
    added to the resulting value."""
    days = None
    operator = operator.strip()
    if operator not in ['<', '<=']:
        raise TypeError('Invalid operator. Expected < or =<. Got {0}'.format(operator))
    if age_upper_range_unit.upper() == 'D':
        days = age_upper_range_value * 1
    elif age_upper_range_unit.upper() == 'M':
        if operator == '<=':
            days = ((1 + age_upper_range_value) * 30) - 1
        else:
            days = age_upper_range_value * 30
    elif age_upper_range_unit.upper() == 'Y':
        if operator == '<=':
            days = ((1 + age_upper_range_value) * 365) - 1
        else:
            days = age_upper_range_value * 365
    else:
        pass
    return days
