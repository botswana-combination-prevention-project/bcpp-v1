from datetime import timedelta
from bhp_visit.models import VisitDefinition


class DateTimeDescriptor(object):
    """For a registered_subject instance only"""
    def __init__(self):
        self.value = None

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if value:
            if isinstance(value, datetime):
                self.value = value
            else:
                raise AttributeError('Can\'t set attribute \'registered_subject\'. Must be an instance of RegisteredSubject. Got %s.' % type(self.registered_subject))        
        else:
            raise AttributeError, "Can't set attribute registered_subject. Got none."                            
            
            
class VisitDefintionDescriptor(object):
    """For a registered_subject instance only"""
    def __init__(self):
        self.value = None

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if value:
            if isinstance(value, VisitDefinition):
                self.value = value
            else:
                raise AttributeError('Can\'t set attribute \'visit_deifinition\'. Must be an instance of VisitDefinition. Got %s.' % type(self.visit_definition))        
        else:
            raise AttributeError, "Can't set attribute visit_definition. Got none."                            
    visit_definition = property(__get__, __set__)

class ApptDateHelper(object):

    appt_datetime  =  ApptDateTimeDescriptor()
    visit_definition  =  VisitDefintionDescriptor()    
    
    def __init__(self, **kwargs):

        #base_appt_datetime = kwargs.get('base_appt_datetime')
        #visit_definition = kwargs.get('visit_definition')
                
    def set_next_appt_datetime(self, **kwargs):    
        
        next_appt_datetime = self.appt_datetime
                
        
    
                
        
        
