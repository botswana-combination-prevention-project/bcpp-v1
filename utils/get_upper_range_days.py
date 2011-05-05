def get_upper_range_days(age_upper_range_value, age_upper_range_unit):
    if age_upper_range_unit.upper() == 'D':
        days = age_upper_range_value * 1
    elif age_upper_range_unit.upper() == 'M':
        days = ((1+age_upper_range_value) * 30)-1
    elif age_upper_range_unit.upper() == 'Y':
        days = ((1+age_upper_range_value) * 365)-1
    else:
        raise TypeError('Invalid age_high_unit in model TestCodeReference, You have the value \'%s\' stored' % (age_upper_range_unit()) )
    return days

