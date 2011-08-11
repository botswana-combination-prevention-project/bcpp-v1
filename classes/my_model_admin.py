from django.db.models import Q
from django.core.urlresolvers import reverse
from bhp_common.models import MyModelAdmin
from bhp_form.models import Appointment,ScheduledEntryBucket
from bhp_registration.models import  RegisteredSubject


class MyRegisteredSubjectModelAdmin (MyModelAdmin):
   
    """ModelAdmin subclass for models with a ForeignKey to 'registered_subject'
    
    Takes care of updating the bucket and redirecting back to the dashboard after
    delete()
    
    """ 
    
    def save_model(self, request, obj, form, change):
        
        ScheduledEntryBucket.objects.update_status(
            model = obj,
            )
                        
        return super(MyRegisteredSubjectModelAdmin, self).save_model(request, obj, form, change)
        
    def delete_model(self, request, obj):

        ScheduledEntryBucket.objects.update_status(
            model = obj,
            action = 'delete',
            )
            
        return super(MyRegisteredSubjectModelAdmin, self).delete_model(request, obj)        

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

        return super(MyRegisteredSubjectModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)                   


    """    
    #override to disallow subject to be changed
    def get_readonly_fields(self, request, obj = None):
        if obj: #In edit mode
            return ('appointment',) + self.readonly_fields
        else:
            return self.readonly_fields  
    """            
