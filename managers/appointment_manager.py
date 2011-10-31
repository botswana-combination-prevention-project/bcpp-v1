import inspect
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models import get_model, Max
from bhp_visit.models import VisitDefinition, ScheduleGroup
from bhp_appointment.models.holiday import Holiday
from bhp_appointment.models.configuration import Configuration

class AppointmentManager(models.Manager):
    
    def create_appointments(self, **kwargs):

        """Create appointments for a registered subject based on a list of visit definitions if given model_name is a member of a schedule group.
    
        1. Only create for visit_instance = 0
        2. If appointment exists, just update the appt_datetime
        
        """
        
        registered_subject = kwargs.get("registered_subject")
        if not registered_subject:
            raise TypeError('AppointmentManager.create_appointments requires registered_subject. Got None')
            
        # this is the model of the membership_form
        model_name = kwargs.get("model_name")
        if not model_name:
            raise TypeError('AppointmentManager.create_appointments requires a model_name. Got None')

        # base_appt_datetime must come from the membership_form model and not from the appt_datetime
        # of the first appointment as the user may change this. 
        # base_appt_datetime = kwargs.get("base_appt_datetime")

        if ScheduleGroup.objects.filter(membership_form__content_type_map__model = model_name):
            # get list of visits for scheduled group containing this model
            # get schedule_group
            schedule_group = ScheduleGroup.objects.get(membership_form__content_type_map__model = model_name)
            # get membership_form of this schedule_group for this registered_subject
            membership_form_model = get_model(app_label=schedule_group.membership_form.content_type_map.app_label, model_name=model_name)
            if membership_form_model.objects.filter(registered_subject=registered_subject):
                # for an existing membership form
                membership_form = membership_form_model.objects.get(registered_subject=registered_subject)
                # determine base_appt_datetime using the membership_form instance
                base_appt_datetime = membership_form.get_registration_datetime()
            else: 
                # we may be calling this method as a new membership for is being inserted   
                # once the instance is saved, the created attribute will = datetime.today()
                base_appt_datetime = datetime.today()            
            
            visit_definitions = VisitDefinition.objects.filter(schedule_group=schedule_group)
            
            for visit_definition in visit_definitions:

                # calculate the appointment date
                if visit_definition.time_point == 0:
                    appt_datetime = self.best_appointment_datetime(appt_datetime=base_appt_datetime)                    
                else:
                    appt_datetime = self.next_appointment_datetime(visit_definition = visit_definition, 
                                                                base_appt_datetime = base_appt_datetime)
                
                # if appt exists, update appt_datetime
                if super(AppointmentManager, self).filter(
                            registered_subject = registered_subject, 
                            visit_definition = visit_definition, 
                            visit_instance = 0):
                    appt = super(AppointmentManager, self).get(
                                registered_subject = registered_subject, 
                                visit_definition = visit_definition, 
                                visit_instance = 0)
                                
                    appt.appt_datetime = appt_datetime

                    appt.save()
                # else create a new appointment                    
                else:
                    super(AppointmentManager, self).create(
                        registered_subject = registered_subject,
                        visit_definition = visit_definition,
                        visit_instance = 0,
                        appt_datetime = appt_datetime,
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
        # check if there are rules to determine a better appt_datetime
        appt_datetime = self.best_appointment_datetime(appt_datetime=next_appt_datetime)
        

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
                    appt_datetime = appt_datetime,
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
        
        
    def next_appointment_datetime(self, **kwargs):

        """ return the appt_datetime given the visit_definition and base_appt_datetime"""

        # should be date from membership form
        base_appt_datetime = kwargs.get('base_appt_datetime')            
        
        if kwargs.get('visit_definition'):
            visit_definition = kwargs.get('visit_definition')
        else:
            raise AttributeError, '%s method %s requires a visit_definition instance OR schedule_group and code' % (self, inspect.stack()[0][3], )             
        
        appt_datetime = base_appt_datetime + VisitDefinition.objects.relativedelta_from_base(visit_definition=visit_definition)
            
        appt_datetime = self.best_appointment_datetime(appt_datetime=appt_datetime, weekday=base_appt_datetime.isoweekday())                                

        return appt_datetime
               
    def check_if_allowed_isoweekday(self,appt_datetime):

        """ check if weekday is allowed, otherwise adjust forward or backward """

        configuration = Configuration.objects.get_configuration()

        # check if is allowable isoweekday based on integer value in 
        # study_specific.allowed_iso_weekdays (e.g. 12345)
        allowed_iso_weekdays = [int(num) for num in str(configuration.allowed_iso_weekdays)]            
        forward = appt_datetime
        while forward.isoweekday() not in allowed_iso_weekdays:
            forward = forward + timedelta(days=+1)                                
        backward = appt_datetime
        while backward.isoweekday() not in allowed_iso_weekdays:
            backward = backward + timedelta(days=-1)                                

        # which is closer to the original appt_datetime
        td_forward = abs(appt_datetime - forward)
        td_backward = abs(appt_datetime - backward)
        if td_forward <= td_backward:
            appt_datetime = forward
        else:
            appt_datetime = backward                                      
        return appt_datetime
        
    def check_if_holiday(self, appt_datetime):

        """ check if appt_datetime lands on a holiday, if so, move forward """

        while appt_datetime.date() in [holiday.holiday_date for holiday in Holiday.objects.all()]:
            appt_datetime = appt_datetime + timedelta(days=+1)
            appt_datetime = self.check_if_allowed_isoweekday(appt_datetime)
        return appt_datetime

    def move_to_same_weekday(self, appt_datetime, weekday=1):

        """ if all appt to land in same day, move """
        if weekday not in range(1,8):
            raise ValueError, 'Weekday must be a number between 1-7, Got %s' % (weekday,)
        # make all appointments land on the same isoweekday, 
        # if possible as date may change becuase of holiday and/or iso_weekday checks below)
        forward = appt_datetime
        while not forward.isoweekday() == weekday:
            forward = forward + timedelta(days=+1)        
        backward = appt_datetime
        while not backward.isoweekday() == weekday:
            backward = backward - timedelta(days=+1)        
        # which is closer to the original appt_datetime
        td_forward = abs(appt_datetime - forward)
        td_backward = abs(appt_datetime - backward)
        if td_forward <= td_backward:
            appt_datetime = forward
        else:
            appt_datetime = backward   

        return appt_datetime
    
        
    def best_appointment_datetime(self, **kwargs):

        """ setup rules to to get a better, but still close, appt_datetime, for example, on the same day as the base, not on holiday, etc. """
        
        appt_datetime = kwargs.get('appt_datetime')
        if not isinstance(appt_datetime, datetime):
            # note, this datetime comes from the membership_form model method get_registration_datetime
            raise TypeError, '%s method %s expects kwarg \'appt_datetime\' to be an instance of datetime, got %s' % (self, inspect.stack()[0][3], appt_datetime.__class__,)
        weekday = kwargs.get('weekday')
        configuration = Configuration.objects.get_configuration()
        
        if weekday and configuration.use_same_weekday:
            appt_datetime = self.move_to_same_weekday(appt_datetime, weekday)           
        appt_datetime = self.check_if_allowed_isoweekday(appt_datetime)

        appt_datetime = self.check_if_holiday(appt_datetime)

        
        # TODO:load balance to a day with fewer appointments
        # 
        #
        
        return appt_datetime

