import sys, socket
from django.core.urlresolvers import reverse
from django.conf.urls.defaults import patterns, include, url
from django.db.models.base import ModelBase
from bhp_common.utils import os_variables
from bhp_entry.models import ScheduledEntryBucket, AdditionalEntryBucket
from bhp_lab_entry.models import ScheduledLabEntryBucket, AdditionalLabEntryBucket
from bhp_appointment.models import Appointment
from bhp_visit.models import ScheduleGroup
from bhp_registration.models import RegisteredSubject
from bhp_dashboard.classes import Dashboard


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
                raise AttributeError('Can\'t set attribute \'registered_subject\'. Must be an instance of RegisteredSubject. Got %s.' % type(self.registered_subject))        
        else:
            raise AttributeError, "Can't set attribute registered_subject. Got none."                            


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
        else:
            raise AttributeError, "Can't set attribute appointment. Got none."                            



class RegisteredSubjectDashboard(Dashboard):
    
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

    registered_subject = RegisteredSubjectDescriptor()

    def __init__(self, **kwargs):
        
        super(RegisteredSubjectDashboard, self).__init__(**kwargs)
                
        self.scheduled_entry_bucket = None
        self.additional_entry_bucket= None
        self.scheduled_lab_bucket = None 
        self.additional_lab_bucket = None       
        self.selected_visit = None 
        self.visit = None
        self.visit_code = None
        self.visit_instance = None                        
        self.visit_model = None
        self.subject_identifier = None
        self.app_label = None
        self.requisition_model = None

    def create(self, **kwargs):
        
        self.registered_subject = kwargs.get('registered_subject', self.registered_subject)
        if self.registered_subject:
            self.subject_type = kwargs.get('subject_type', self.registered_subject.subject_type)

            # subject identifier is almost always available
            self.subject_identifier = self.registered_subject.subject_identifier
            self.dashboard_identifier = self.subject_identifier            
            if not self.subject_identifier:
                # but if not, check for registration_identifier
                self.subject_identifier = self.registered_subject.registration_identifier                
                self.dashboard_identifier = "%s [%s] %s" % (self.registered_subject.first_name, self.registered_subject.initials, self.registered_subject.gender,)
            if not self.subject_identifier:                        
                raise AttributeError, "RegisteredSubjectDashboard requires a subject_identifier. RegisteredSubject has no identifier for this subject." 
            
            
            self.context.add(
                        registered_subject = self.registered_subject,
                        subject_identifier = self.subject_identifier,
                        subject_type = self.subject_type,
                        )            

        super(RegisteredSubjectDashboard, self).create(**kwargs)
                
        self.visit_code = kwargs.get('visit_code', self.visit_code)
        self.visit_instance = kwargs.get("visit_instance", self.visit_instance)                
        self.visit_model = kwargs.get('visit_model', self.visit_model)
        self.context.add(
                    visit_model = self.visit_model,
                    visit_instance = self.visit_instance,
                    visit_code = self.visit_code,
                    )            

        if not self.requisition_model:
            raise AttributeError('RegisteredSubjectDashboard.create() requires attribute \'requisition_model\'. Got none.')
            #elif not isinstance(self.visit_model, ModelBase):
            #    raise AttributeError('RegisteredSubjectDashboard.create() requires attribute \'visit_model\' be type ModelBase. Got %s.' % type(self.visit_model))            


        if not self.visit_model:
            raise AttributeError('RegisteredSubjectDashboard.create() requires attribute \'visit_model\'. Got none.')
            #elif not isinstance(self.visit_model, ModelBase):
            #    raise AttributeError('RegisteredSubjectDashboard.create() requires attribute \'visit_model\' be type ModelBase. Got %s.' % type(self.visit_model))            
        else:
            self.visit_model_name = self.visit_model._meta.module_name
            self.context.add(visit_model_name = self.visit_model_name)            
            
            self.visit_model_app_label = self.visit_model._meta.app_label
            self.context.add(visit_model_app_label = self.visit_model_app_label)                    
            try:
                self.visit_model_add_url = reverse('admin:%s_%s_add' % (self.visit_model_app_label, self.visit_model_name))
            except:
                # model must be registered in admin
                raise ValueError, 'NoReverseMatch: Reverse for \'%s_%s_add\'. Check model is registered in admin' % (self.visit_model_app_label, self.visit_model_name)   
            self.context.add(visit_model_add_url = self.visit_model_add_url)                    

        
        self.set_membership_forms()

        self.set_appointments()
            
        self.set_additional_entry_bucket()

        self.set_scheduled_entry_bucket()
        
        self.set_scheduled_lab_bucket()        

        self.set_additional_lab_bucket()        
        
        self.set_current_appointment()
        
        self.set_current_visit()
        
        # update / add to entries in ScheduledEntryBucket, ScheduledLabEntryBucket
        if self.visit:
            ScheduledEntryBucket.objects.add_for_visit(visit_model_instance = self.visit)           
                     
            # if requisition_model has been defined, assume scheduled labs otherwise pass
            if hasattr(self, 'requisition_model'):
                ScheduledLabEntryBucket.objects.add_for_visit(
                    visit_model_instance = self.visit,
                    requisition_model = self.requisition_model,
                    )
        

    def set_scheduled_entry_bucket(self):
    
        # get list of scheduled crfs
        if self.visit_code:
            # filter for appointment with visit_instance=0
            appointment = Appointment.objects.get(
                                        registered_subject = self.registered_subject, 
                                        visit_definition__code = self.visit_code, 
                                        visit_instance = 0,
                                        )
            self.scheduled_entry_bucket = ScheduledEntryBucket.objects.get_scheduled_forms_for(
                registered_subject = self.registered_subject, 
                appointment = appointment,    
                visit_code = self.visit_code,
                )  


        self.context.add(scheduled_entry_bucket = self.scheduled_entry_bucket)

    
    def set_scheduled_lab_bucket(self):

        # get list of scheduled crfs
        if self.visit_code:
            # filter for appointment with visit_instance=0
            appointment = Appointment.objects.get(
                                        registered_subject = self.registered_subject, 
                                        visit_definition__code = self.visit_code, 
                                        visit_instance = 0,
                                        )
            self.scheduled_lab_bucket = ScheduledLabEntryBucket.objects.get_scheduled_labs_for(
                registered_subject = self.registered_subject, 
                appointment = appointment,    
                visit_code = self.visit_code,
                )  

        self.context.add(scheduled_lab_bucket = self.scheduled_lab_bucket)                                                      

    def set_additional_lab_bucket(self):

        # get list of scheduled crfs
        if self.visit_code:
            # filter for appointment with visit_instance=0
            appointment = Appointment.objects.get(
                                        registered_subject = self.registered_subject, 
                                        visit_definition__code = self.visit_code, 
                                        visit_instance = 0,
                                        )
            self.additional_lab_bucket = AdditionalLabEntryBucket.objects.get_labs_for(
                registered_subject = self.registered_subject, 
                appointment = appointment,    
                )  

        self.context.add(additional_lab_bucket = self.additional_lab_bucket)                                                      
            
    def set_appointments(self):

        # get all appointments for this registered_subject 
        # if self.visit_code and self.visit_instance, then limit to the one appointment
        if self.visit_code and self.visit_instance:        
            self.appointments = Appointment.objects.filter(registered_subject=self.registered_subject, visit_definition__code=self.visit_code, visit_instance=self.visit_instance)            
        else:
            self.appointments = Appointment.objects.filter(registered_subject = self.registered_subject).order_by('appt_datetime', 'visit_definition__code', 'visit_instance')
        self.context.add(appointments = self.appointments)                
    

    def set_current_visit(self):
    
        if self.appointment:
            # set the visit
            if self.visit_model:
                self.visit = self.visit_model.objects.get(appointment = self.appointment)                    
            else:
                raise AttributeError('Cannot determine attribute \'visit_model\' in RegisteredSubjectDashboard. Got none. Either pass as a attribute or add_to_context')        
        else:
            self.visit = self.visit_model.objects.none()

        self.context.add(visit = self.visit)                    
        

    def set_current_appointment(self):
    
        self.appointment = Appointment.objects.none()
    
        # get the appointment that has focus based on visit_code
        if self.visit_code:
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
                
        self.context.add(appointment = self.appointment)                    

        
    def set_additional_entry_bucket(self):

        # get additional crfs
        self.additional_entry_bucket= AdditionalEntryBucket.objects.filter(
            registered_subject = self.registered_subject
            )
        self.context.add(additional_entry_bucket = self.additional_entry_bucket)
                                        

    def set_membership_forms(self):

        # add membership forms for this registered_subject and subject_type
        # these are the KEYED, UNKEYED schedule group membership forms
        self.membership_forms = ScheduleGroup.objects.get_membership_forms_for(
            registered_subject = self.registered_subject,
            membership_form_category = self.subject_type,
            )

        self.context.add(membership_forms = self.membership_forms)                    
        self.context.add(
            keyed_membership_forms = self.membership_forms['keyed'],        
            unkeyed_membership_forms = self.membership_forms['unkeyed'],
            )

    def get_urlpatterns(self, view, regex, **kwargs):
    
        """ generate urls, add this to your urls.py of your local dashboard app
        
            regex = {}
            regex['dashboard_type'] = 'subject'
            regex['subject_identifier'] = 'S[0-9]{6}\-[0-9]{2}\-[A-Z]{3}[0-9]{2}'
            regex['visit_code'] = '\w+'
            regex['visit_instance'] = '[0-9]{1}'
            subject_dashboard = SubjectDashboard()
            urlpatterns = subject_dashboard.get_urlpatterns('mochudi_survey_dashboard.views', regex, visit_field_names=['subject_visit',])
            
            
        """        
    
        regex['pk'] = '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}'
        regex['content_type_map'] = '\w+'
        
        
        visit_field_names =  kwargs.get('visit_field_names', ['visit'])

        if 'registration_identifier' not in regex.keys():
            regex['registration_identifier'] = '[A-Z0-9]{6,8}'             

        self.urlpatterns = patterns(view,

            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<panel>\d+)/$'.format(**regex), 
                'dashboard', 
                name="dashboard_visit_url"
                ),

            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<appointment>{pk})/$'.format(**regex), 
                'dashboard', 
                name="dashboard_visit_url"
                ),

            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/$'.format(**regex), 
                'dashboard', 
                name="dashboard_visit_url"
                ),

            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/$'.format(**regex), 
                'dashboard', 
                name="dashboard_visit_url"
                ),
            )                

        for visit_field_name in visit_field_names:

            regex['visit_field_name'] = visit_field_name
            self.urlpatterns += patterns(view,
            
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<{visit_field_name}>{pk})/(?P<panel>\d+)/$'.format(**regex), 
                    'dashboard', 
                    name="dashboard_visit_add_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<{visit_field_name}>{pk})/$'.format(**regex), 
                    'dashboard', 
                    name="dashboard_visit_add_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<{visit_field_name}>{pk})/$'.format(**regex), 
                    'dashboard', 
                    name="dashboard_visit_add_url"
                    ),
                )    

            
        self.urlpatterns += patterns(view,
        
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<content_type_map>{content_type_map})/$'.format(**regex), 
                'dashboard', 
                name="dashboard_visit_url"
                ),


            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/$'.format(**regex), 
                'dashboard', 
                name="dashboard_url"
                ),
                
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<appointment>{pk})/$'.format(**regex), 
                'dashboard', 
                name="dashboard_url"
                ),
                
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<registered_subject>{pk})/$'.format(**regex), 
                'dashboard', 
                name="dashboard_url"
                ),

            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<registration_identifier>{registration_identifier})/(?P<registered_subject>{pk})/$'.format(**regex), 
                'dashboard', 
                name="dashboard_url"
                ),

            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<registered_subject>{pk})/$'.format(**regex), 
                'dashboard', 
                name="dashboard_url"
                ),

            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<registration_identifier>{registration_identifier})/$'.format(**regex), 
                'dashboard', 
                name="dashboard_url"
                ),

            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<registered_subject>{pk})/(?P<visit_definition>{pk})/(?P<visit_instance>{visit_instance})/$'.format(**regex), 
                'dashboard', 
                name="dashboard_url"
                ),

            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<registered_subject>{pk})/(?P<subject_consent>{pk})/$'.format(**regex), 
                'dashboard', 
                name="dashboard_url"
                ),

            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<pk>{pk})/$'.format(**regex), 
                'dashboard', 
                name="pk_dashboard_url"
                ),

            )
        return self.urlpatterns

        
