from django.db import models
from django.db.models import get_model, Max
from bhp_visit.models import VisitDefinition, ScheduleGroup
from bhp_appointment.classes import ApptDateHelper


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
                
                # calculate the appointment date based on the 
                
                
            
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

        #return visits

    def delete_appointments_for_model(self, **kwargs):        
        
        """ delete created appointments for this registered_subject for this model_name if visit report not yet submitted """
        
        registered_subject = kwargs.get("registered_subject")
        if not registered_subject:
            raise TypeError('AppointmentManager.delete_appointments requires registered_subject. Got None')
        model_name = kwargs.get("model_name")
        if not model_name:
            raise TypeError('AppointmentManager.delete_appointments requires a model_name. Got None')
        visit_model_name = kwargs.get("visit_model_name")
        if not model_name:
            raise TypeError('AppointmentManager.delete_appointments requires a visit_model_name. Got None')
        visit_model_app_label = kwargs.get("visit_model_app_label")
        if not model_name:
            raise TypeError('AppointmentManager.delete_appointments requires a visit_model_app_label. Got None')

        visit_definitions = self.list_visit_definitions_for_model(registered_subject=registered_subject, model_name=model_name)            
        
        # only delete appointments without a visit model 
        visit_model = get_model( visit_model_app_label, visit_model_name)
        appointments = super(AppointmentManager, self).filter(registered_subject=registered_subject, visit_definition__in=visit_definitions)    
        count = 0
        for appointment in appointments:
            if not visit_model.objects.filter(appointment=appointment):
                appointment.delete()   
                count += 1
        
        return count

    def create_next_appointment_instance(self, **kwargs):
    
        """ create the next instance of an appointment given the base appointment instance (.0) and the next appt_datetime """
    
        appointment = kwargs.get('base_appointment')
        next_appt_datetime = kwargs.get('next_appt_datetime')

        if not super(AppointmentManager, self).filter(
                                                registered_subject=appointment.registered_subject, 
                                                visit_definition=appointment.visit_definition, 
                                                appt_datetime=next_appt_datetime): 
            
            # what was the last instance created?
            aggr = super(AppointmentManager, self).filter(
                                                    registered_subject=appointment.registered_subject, 
                                                    visit_definition=appointment.visit_definition
                                                    ).values('visit_instance').annotate(Max('visit_instance')).order_by()
            if aggr:
                next_visit_instance = int(aggr[0]['visit_instance__max'] + 1)
                super(AppointmentManager, self).create(
                    registered_subject = appointment.registered_subject,
                    visit_definition = appointment.visit_definition,
                    visit_instance = next_visit_instance,
                    appt_datetime = next_appt_datetime,
                    )

    def list_appointments_for_model(self, **kwargs):        
        
        """ list created appointments for this registered_subject for this model_name """
        
        registered_subject = kwargs.get("registered_subject")
        if not registered_subject:
            raise TypeError('AppointmentManager.list_appointments requires registered_subject. Got None')
        model_name = kwargs.get("model_name")
        if not model_name:
            raise TypeError('AppointmentManager.list_appointments requires a model_name. Got None')

        visit_definitions = self.list_visit_definitions_for_model(registered_subject=registered_subject, model_name=model_name)            
            
        appointments = super(AppointmentManager, self).filter(registered_subject=registered_subject, visit_definition__in=visit_definitions)    

        return appointments            
            

    def list_visit_definitions_for_model(self, **kwargs):        
        
        """ list visit_definitions for which appointments would be created or updated for this model_name"""
        
        registered_subject = kwargs.get("registered_subject")
        if not registered_subject:
            raise TypeError('AppointmentManager.list_visit_deinitions requires registered_subject. Got None')
            
        model_name = kwargs.get("model_name")
        if not model_name:
            raise TypeError('AppointmentManager.list_visit_deinitions requires a model_name. Got None')
        if ScheduleGroup.objects.filter(membership_form__content_type_map__model = model_name): 
            # get list of visits for scheduled group containing this model
            visit_definitions = VisitDefinition.objects.filter(schedule_group = ScheduleGroup.objects.get(membership_form__content_type_map__model = model_name))
        else:
            visit_definitions = None

        return visit_definitions            
            
                        
