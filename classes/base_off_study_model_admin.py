from base_registered_subject_model_admin import BaseRegisteredSubjectModelAdmin
from bhp_appointment.models import Appointment

class BaseOffStudyModelAdmin(BaseRegisteredSubjectModelAdmin): 

    def save_model(self, request, obj, form, change):
        
        # delete future appointments
        Appointment.objects.filter(
            registered_subject=obj.registered_subject, 
            appt_datetime__gt=obj.offstudy_datetime, 
            ).extra(where=[self.visit_model_name+'=%s'], params=[True]).delete()    
    
        super(BaseOffStudyModelAdmin, self).save_model(request, obj, form, change)
