from django.db import models
from bhp_visit.models import VisitDefinition, ScheduleGroup

class AppointmentManager(models.Manager):
    
    def create_appointments(self, **kwargs):

        """Create appointments for a registered subject based on a list of visit definitions if given model_name is a member of a schedule group.
    
        1. Only create for visit_instance = 0
        2. If appointment exists, just update the appt_datetime
        
        """
        
        registered_subject = kwargs.get("registered_subject")
        if not registered_subject:
            raise TypeError('AppointmentManager.create_appointments requires registered_subject. Got None')
            
        model_name = kwargs.get("model_name")
        if not model_name:
            raise TypeError('AppointmentManager.create_appointments requires a model_name. Got None')
        
        base_appt_datetime = kwargs.get("base_appt_datetime")

        if ScheduleGroup.objects.filter(membership_form__content_type_map__model = model_name):
            # get list of visits for scheduled group containing this model
            visits = VisitDefinition.objects.filter(schedule_group = ScheduleGroup.objects.get(membership_form__content_type_map__model = model_name))
            #raise TypeError()
            for visit in visits:
                # if appt exists, update appt_datetime
                if super(AppointmentManager, self).filter(
                            registered_subject = registered_subject, 
                            visit_definition = visit, 
                            visit_instance = 0):
                    appt = super(AppointmentManager, self).get(
                                registered_subject = registered_subject, 
                                visit_definition = visit, 
                                visit_instance = 0)
                    appt.appt_datetime = base_appt_datetime
                    appt.save()
                # else create a new appointment                    
                else:
                    super(AppointmentManager, self).create(
                        registered_subject = registered_subject,
                        visit_definition = visit,
                        visit_instance = 0,
                        appt_datetime = base_appt_datetime,
                        )


