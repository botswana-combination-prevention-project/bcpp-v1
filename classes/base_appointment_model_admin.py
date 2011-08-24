from django.db.models import Q, ForeignKey
from django.core.urlresolvers import reverse
from bhp_common.models import MyModelAdmin
from bhp_entry.models import ScheduledEntryBucket
from bhp_appointment.models import Appointment

class BaseAppointmentModelAdmin(MyModelAdmin):

    """ModelAdmin subclass for models with a ForeignKey to 'appointment'. """ 

    def __init__(self, *args, **kwargs):
        
        super(BaseAppointmentModelAdmin, self).__init__(*args, **kwargs)

    def save_model(self, request, obj, form, change):

        return super(BaseAppointmentModelAdmin, self).save_model(request, obj, form, change)
        
    def delete_model(self, request, obj):

        return super(BaseAppointmentModelAdmin, self).delete_model(request, obj) 

    def delete_view(self, request, object_id, extra_context=None):

        subject_identifier = self.form.appointment.registered_subject.subject_identifier
        result = super(BaseAppointmentModelAdmin, self).delete_view(request, object_id, extra_context)
        result['Location'] = reverse('dashboard_url' , kwargs={'dashboard_type':'subject', 'subject_identifier':subject_identifier})

        return result
        
    #override, limit dropdown in add_view to id passed in the URL        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        if db_field.name == 'appointment' and request.GET.get('appointment'):
            kwargs["queryset"] = Appointment.objects.filter(pk = request.GET.get('appointment', 0))                                                        
            
        return super(BaseAppointmentModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)   
