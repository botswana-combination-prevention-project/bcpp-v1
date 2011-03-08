from datetime import date

from django import template

register = template.Library()

@register.filter(name='age')
def age(birth_date):
    today = date.today()
    try: # raised when birth date is February 29 and the current year is not a leap year
        birthday = born.replace(year=today.year)
    except ValueError:
        birthday = born.replace(year=today.year, day=born.day-1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year

@register.filter(name='gender')
def gender(value):
    if 'F':
        return 'Female'
    if 'M':
        return 'Male'
    else:
        return value    

