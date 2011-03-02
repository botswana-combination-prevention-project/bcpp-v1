from bhp_registration.models import RegisteredSubject
from models import VisitDefinition
from models import Appointment

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

