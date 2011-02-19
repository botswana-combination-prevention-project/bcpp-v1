import re, socket, sys
from geopy import Point
from geopy.distance import distance, VincentyDistance
from django import forms
from django.core.exceptions import ValidationError


def check_initials_field(first_name, last_name, initials):
    """
        check that the first and last initials match what is expected based on 
        first and last name
        
    """
    if initials != None and first_name != None:
        if first_name[:1] != initials[:1]:
            raise forms.ValidationError("First initial does not match first name, expected '%s' but you wrote %s." % (first_name[:1], initials[:1]))
            
    if initials != None and last_name != None:
        if last_name[:1] != initials[-1:]:
            raise forms.ValidationError("Last initial does not match last name, expected '%s' but you wrote %s." % (last_name[:1], initials[-1:]))
            
def check_omang_field(omang, gender):            
    str_value = "%s" % (omang)
    pattern = ""
    if gender=='M':
        pattern = '^[0-9]{4}[1]{1}[0-9]{4}$'
    if gender=='F':
        pattern = '^[0-9]{4}[2]{1}[0-9]{4}$'        

    if pattern:
        p = re.compile(pattern)
        if p.match(str_value) == None:
            raise ValidationError(u'Invalid Omang number. You entered %s.' % (str_value))
            
def os_variables():
            
    a = {}
    a['hostname'] = socket.gethostname()
    
    return a


def distance_from_gps(lat1, lon1):
    return VincentyDistance(miles=distMiles).destination(Point(lat1, lon1), bearing)
    
            
