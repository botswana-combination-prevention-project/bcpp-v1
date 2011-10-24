from datetime import datetime
from django.db.models import Q
from django.core.urlresolvers import reverse
from bhp_common.models import MyModelAdmin
from bhp_export_data.actions import export_as_csv_action
from bhp_appointment.models import Appointment
from bhp_entry.models import ScheduledEntryBucket, AdditionalEntryBucket
from bhp_registration.models import  RegisteredSubject


class BaseRegisteredSubjectModelAdmin (MyModelAdmin):
   
    """ModelAdmin subclass for models with a ForeignKey to 'registered_subject'
    
    Takes care of updating the bucket and redirecting back to the dashboard after
    delete()
    
    """ 
    
    def save_model(self, request, obj, form, change):
    
        #if model is in a member of a schedule group, create appointments
        Appointment.objects.create_appointments( 
            registered_subject = obj.registered_subject, 
            base_appt_datetime = datetime.today(), 
            model_name = self.model.__name__.lower(),
            )
        
        AdditionalEntryBucket.objects.update_status(
            registered_subject = obj.registered_subject,    
            model_instance = obj,
            )
                       
        return super(BaseRegisteredSubjectModelAdmin, self).save_model(request, obj, form, change)
        
    def delete_model(self, request, obj):

        AdditionalEntryBucket.objects.update_status(
            registered_subject = obj.registered_subject,    
            model_instance = obj,
            action = 'delete',
            )

        return super(BaseRegisteredSubjectModelAdmin, self).delete_model(request, obj)        

    def delete_view(self, request, object_id, extra_context=None):
        
        # you can specify an attribute other than 'subject_identifier'
        # by declaring self.subject_identifier_attribute at the ModelAdmin class declaration
        # as long as the attribute exists in registered subject
        if not 'subject_identifier_attribute' in self.__class__.__dict__:
            subject_identifier_attribute = 'subject_identifier'
        else:
            subject_identifier_attribute = self.subject_identifier_attribute

        if not subject_identifier_attribute in self.model.objects.get(pk=object_id).registered_subject.__dict__:
            raise AttributeError, 'Attribute %s does not exist in model RegisteredSubject. Check the value set in your ModelAdmin for model %s' % (subject_identifier_attribute, self.model._meta.module_name,)
        subject_identifier = self.model.objects.get(pk=object_id).registered_subject.__dict__[subject_identifier_attribute]        

        result = super(BaseRegisteredSubjectModelAdmin, self).delete_view(request, object_id, extra_context)

        result['Location'] = reverse('dashboard_url' , kwargs={'dashboard_type':self.dashboard_type, 'subject_identifier':subject_identifier})

        return result


    #override, limit dropdown in add_view to id passed in the URL        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "appointment":
            if request.GET.get('appointment'):
                kwargs["queryset"] = Appointment.objects.filter(id__exact=request.GET.get('appointment'))
            #elif self.model.objects.filter(pk=object_id):
            #    kwargs["queryset"] = Appointment.objects.filter(pk=self.model.objects.get(pk=object_id).appointment.pk)
            else:
                kwargs["queryset"] = Appointment.objects.none()

        if db_field.name == "registered_subject":
            if request.GET.get('registered_subject'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(pk = request.GET.get('registered_subject'))
            #elif self.model.objects.filter(pk=object_id):
            #    kwargs["queryset"] = RegisteredSubject.objects.filter(pk = self.model.objects.get(pk=object_id).appointment.registered_subject.pk)
            else:
                kwargs["queryset"] = RegisteredSubject.objects.none()

        return super(BaseRegisteredSubjectModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)                   


    actions = [export_as_csv_action("CSV Export of registered_subject", 
        fields=[], 
        exclude=[],
        extra_fields=[
            {'subject_identifier': 'registered_subject__subject_identifier'},
            {'gender': 'registered_subject__gender'},
            {'dob': 'registered_subject__dob'},
            {'registered': 'registered_subject__registration_datetime'},                                                                                    
            ],
        )]
        
    search_fields = ('registered_subject__subject_identifier',) 
    
    list_display = ('registered_subject', 'created', 'modified', 'user_created', 'user_modified',)    
    
    list_filter = (
        'registered_subject__gender', 
        'created', 
        'modified', 
        'user_created',
        'user_modified',
        )

