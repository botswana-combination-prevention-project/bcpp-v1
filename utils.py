from bhp_registration import RegisteredSubject
from bhp_visit.models import VisitDefinition
from bhp_visit.models import Appointment

def create_appointment(subject, appt_datetime, visit_definition):

    visit_instance
    
    #search for registered subject
    registered_subject = RegisteredSubject.objects.filter()

    ObjAppt = Appointment(    
        registered_subject=, 
        appt_datetime=, 
        visit_definition=,
        )
    
    ObjAppt.save()
    
    return ObjAppt

