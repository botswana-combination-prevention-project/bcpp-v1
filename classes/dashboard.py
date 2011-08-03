import sys, socket
from django.contrib.auth.decorators import login_required
from bhp_common.utils import os_variables
from bhp_form.models import ScheduledEntryBucket, AdditionalEntryBucket, Appointment, ScheduleGroup
from bhp_registration.models import RegisteredSubject

class ContextDescriptor(object):
    """Descriptior for a registered subject dashboard context"""    
    def __init__(self):
        self.context = {}
        self.exclude_keys = []
        self.initialized = False
    def initialize(self,obj):    
        self.context = {
            "search_name": obj.search_name,
            "dashboard": obj.dashboard_type,
            "keyed_membership_forms": obj.membership_forms['keyed'],        
            "unkeyed_membership_forms": obj.membership_forms['unkeyed'],
            "appointments": obj.appointments,
            "appointment": obj.appointment,        
            "registered_subject": obj.registered_subject,
            "subject_identifier": obj.subject_identifier,
            "scheduled_entry_bucket": obj.scheduled_crfs,
            "additional_entry_bucket": obj.additional_crfs,        
            "visit": obj.visit,        
            "visit_code": obj.visit_code,
            "visit_instance": obj.visit_instance,                
            "hostname": socket.gethostname(),
            "os_variables":os_variables(),
            }        
        self.initialized = True            
    def __get__(self, instance, owner):
        return self.context
    def __set__(self, instance, arg):
        """Accept a dictionary with either the Dashboard object to initialize the contect OR k,v pairs to add to the context."""        
        if arg and isinstance(arg, Dashboard):
            self.initialize(arg)
        elif arg and isinstance(arg, dict) and self.initialized: 
            # k,v pairs should be passed only after you have initialized context
            for k,v in arg.items():
                if k == 'exclude_from_context':
                    # this key hold a list of keys to delete from the context
                    self.exclude_keys.append(v)
                else:
                    self.context[k] = v
            if self.exclude_keys:
                for j in self.context.keys():
                    if j in self.exclude_keys:
                        del self.context[j]
        else:
            if not self.initialized:
                raise AttributeError, "Can't add dashboard dict key, value pair for \'context\'. Context has not been initialized()."
            else:    
                raise AttributeError, "Can't set/add dashboard  dict key, value pair for attribute \'context\'. Got key=%s, value=%s" % (self.name, key, value)

class RegisteredSubjectDescriptor(object):
    """For a registered_subject instance only"""
    def __init__(self):
        self.value = RegisteredSubject.objects.none()

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if value:
            if isinstance(value, RegisteredSubject):
                self.value = value
            else:
                raise AttributeError, "Can't set attribute registered_subject. Must be an instance of RegisteredSubject"
        else:
            raise AttributeError, "Can't set dashboard attribute registered_subject. Got none."                            

class AppointmentDescriptor(object):
    """For an appointment instance only"""
    def __init__(self):
        self.name = ''
        self.re = r''
        self.msg = ''
        self.value = Appointment.objects.none()
    def __get__(self, instance, owner):
        return self.value
    def __set__(self, instance, value):
        if value:
            if isinstance(value, Appointment):
                self.value = value
            else:
                raise AttributeError, "Can't set attribute %s. Must be an instance of Appointment" % (self.name)


class Dashboard(object):
    
    """
    Create and add to a default clinic "registered subject" dashboard context and render_to_response from a view.
    
    In your view:
    
    #get request vars from kwargs, lookup others from your models as required
    ...
    ...
    if kwargs.get('subject_identifier'):
        registered_subject = RegisteredSubject.objects.get(subject_identifier = kwargs.get('subject_identifier'))
    ...    

    # create dashboard object
    dashboard = Dashboard()
    
    # create a basic dashboard context
    dashboard.create(
        registered_subject = registered_subject, # get this instance when you are handling request vars
        visit_code = kwargs.get('visit_code'),
        visit_instance = kwargs.get("visit_instance"),              
        visit_model = InfantVisit, # for example ...
    )

    # add extra context
    dashboard.add_to_context({'search_name': 'infantbirth'})

    # render_to_response
    return render_to_response(
        dashboard.template, # template name is assumed unless you set it deliberately
        dashboard.context,
        context_instance=RequestContext(request))     
    ...
    ...
    """


    context = ContextDescriptor()
    registered_subject = RegisteredSubjectDescriptor()
    #subject_identifier = SubjectIdentifierDescriptor()

    def __init__(self, **kwargs):
        
        self.scheduled_crfs = None
        self.additional_crfs = None
        self.selected_visit = None   

        self.exclude_from_context = ['template',]        

    def __unicode__(self):
        return self.context

    def add_to_context(self, dct):
        if isinstance(dct, dict):
            self.context = dct
        else:
            raise AttributeError, "Can't set dashboard context attribute. Add_to_context() expects a dictionary"    
            
    def create(self, **kwargs):

        self.registered_subject = kwargs.get('registered_subject')
        self.subject_identifier = self.registered_subject.subject_identifier
        self.subject_type = kwargs.get('subject_type', self.registered_subject.subject_type)
        self.visit_code = kwargs.get('visit_code')
        self.visit_instance = kwargs.get("visit_instance")                
        self.visit_model = kwargs.get('visit_model')
        self.visit = self.visit_model.objects.none()
        self.search_name = kwargs.get('search_name')

        self.dashboard_type = kwargs.get('dashboard_type', self.subject_type.lower())        
        self.template = kwargs.get('template', '%s_dashboard.html' % self.dashboard_type)        
        

        # add membership forms for this registered_subject and subject_type
        # these are the KEYED, UNKEYED schedule group membership forms
        self.membership_forms = ScheduleGroup.objects.get_membership_forms_for(
            registered_subject = self.registered_subject,
            membership_form_category = self.subject_type,
            )
        
        # get all appointments for this registered_subject    
        self.appointments = Appointment.objects.filter(registered_subject = self.registered_subject).order_by('visit_definition__code', 'visit_instance')
            
        # get additional crfs
        self.additional_crfs = AdditionalEntryBucket.objects.filter(
            registered_subject = self.registered_subject
            )

        # get the appointment that has focus based on visit_code
        if self.visit_code:
            # get list of scheduled crfs
            # do not filter for visit_instance as this does not apply for scheduled_crfs
            self.scheduled_crfs = ScheduledEntryBucket.objects.get_scheduled_forms_for(
                registered_subject = self.registered_subject, 
                visit_code = self.visit_code,
                )            
            
            # get visit associated with this appointment (in progress) and visit code and instance
            if Appointment.objects.filter(registered_subject=self.registered_subject, 
                                        visit_definition__code = self.visit_code, 
                                        visit_instance = self.visit_instance,):            

                # set the appointment
                self.appointment = Appointment.objects.get(
                    registered_subject = self.registered_subject, 
                    visit_definition__code = self.visit_code,
                    visit_instance = self.visit_instance,                 
                    )

                # set the visit
                self.visit = self.visit_model.objects.get(appointment = self.appointment)

        else:
            # no appointment selected because there is no visit_code
            self.appointment = Appointment.objects.none()    
            
        
        # initialize dashboard context with current "self" variables less those listed in self.exclude_from_context
        self.context = self

