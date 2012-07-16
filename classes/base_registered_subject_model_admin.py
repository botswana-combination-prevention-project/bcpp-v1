from django.core.urlresolvers import reverse
try:
    from bhp_crypto.classes import BaseCrypterModelAdmin as BaseModelAdmin
except ImportError:
    from bhp_base_model.classes import BaseModelAdmin
from bhp_export_data.actions import export_as_csv_action
from bhp_registration.models import RegisteredSubject
from bhp_appointment.models import Appointment
from bhp_entry.models import AdditionalEntryBucket


class BaseRegisteredSubjectModelAdmin (BaseModelAdmin):
   
    """ModelAdmin subclass for models with a ForeignKey to 'registered_subject'
    
    Takes care of updating the bucket and redirecting back to the dashboard after
    delete()
    
    """ 
    
    def __init__(self, *args, **kwargs):

        self.search_fields = ['registered_subject__subject_identifier','registered_subject__sid'] 
    
        self.list_display = ['registered_subject', 'created', 'modified', 'user_created', 'user_modified',]    
    
        self.list_filter = [
            'registered_subject__gender', 
            'registered_subject__study_site',
            'registered_subject__hiv_status',
            'registered_subject__survival_status',
            'registered_subject__registration_datetime',                                                                                    
            'created', 
            'modified', 
            'user_created',
            'user_modified',
            'hostname_created',
            'hostname_modified',
            ]
            
        super(BaseRegisteredSubjectModelAdmin, self).__init__(*args, **kwargs)            



    def save_model(self, request, obj, form, change):
        
        # i am explicitly listing valid subclasses for now. in future when code has stabilized
        # might be able to remove this ... i just want to know who's coming in here.
        #if not issubclass(obj.__class__, (BaseRegisteredSubjectModel, BaseOffStudy, BaseDeathReport)):
        #    raise TypeError('%s is using BaseRegisteredSubjectModelAdmin but is not a subclasses of BaseRegisteredSubjectModel.' % (obj, ))

        if not 'registered_subject' in [fld.name for fld in self.model._meta.fields]:
            raise TypeError('%s is using BaseRegisteredSubjectModelAdmin but does not have a key to RegisteredSubject.' % (obj, ))

        # note: appointments are create in the base model's save() method
        # as long as it inherets from BaseRegisteredSubjectModel() 
                               
        return super(BaseRegisteredSubjectModelAdmin, self).save_model(request, obj, form, change)
        
    def delete_model(self, request, obj):

        AdditionalEntryBucket.objects.update_status(
            registered_subject = obj.registered_subject,    
            model_instance = obj,
            action = 'delete',
            )

        return super(BaseRegisteredSubjectModelAdmin, self).delete_model(request, obj)        

    def delete_view(self, request, object_id, extra_context=None):
        
        kwargs={'dashboard_type':self.dashboard_type}
        # you can specify an attribute other than 'subject_identifier'
        # by declaring self.subject_identifier_attribute at the ModelAdmin class declaration
        # as long as the attribute exists in registered subject
        subject_identifier_attribute = 'subject_identifier'
        if 'subject_identifier_attribute' in self.__class__.__dict__:
            subject_identifier_attribute = self.subject_identifier_attribute
        if not subject_identifier_attribute in self.model.objects.get(pk=object_id).registered_subject.__dict__:
            raise AttributeError, 'Attribute %s does not exist in model RegisteredSubject. Check the value set in your ModelAdmin for model %s' % (subject_identifier_attribute, self.model._meta.module_name,)
        subject_identifier = self.model.objects.get(pk=object_id).registered_subject.__dict__[subject_identifier_attribute]        
        if subject_identifier:
            kwargs['subject_identifier'] = subject_identifier
        else:    
            # if subject_identifier not yet allocated, try registration_identifier
            kwargs['registered_subject'] = self.model.objects.get(pk=object_id).registered_subject.pk                
            
        result = super(BaseRegisteredSubjectModelAdmin, self).delete_view(request, object_id, extra_context)

        result['Location'] = reverse('dashboard_url', kwargs=kwargs)

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
        


