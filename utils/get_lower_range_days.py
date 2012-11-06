
def get_lower_range_days(age_lower_range_value, age_low_range_unit):
    days = None
    if age_low_range_unit.upper() == 'D':
        days = age_lower_range_value * 1
    elif age_low_range_unit.upper() == 'M':
        days = ((1+age_lower_range_value) * 30)-1
    elif age_low_range_unit.upper() == 'Y':
        days = ((1+age_lower_range_value) * 365)-1
    else:
        pass
        #raise TypeError('Invalid age_low_unit in model TestCodeReference, You have the value \'%s\' stored' % (age_low_range_unit.upper()))
    return days

