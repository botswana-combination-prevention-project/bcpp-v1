from django.db.models import get_model
#from django.contrib import messages
from bhp_bucket.classes import bucket
from bhp_appointment.models import BaseAppointmentTracking

def update_entry_bucket_rules(modeladmin, request, queryset):
    ScheduledEntryBucket = get_model('bhp_entry', 'scheduledentrybucket')
    for qs in queryset:
        if isinstance(qs, BaseAppointmentTracking):
            #ScheduledEntryBucket.objects.add_for_visit(visit_model_instance=qs)
            bucket.update_all(qs) 
        else:
            modeladmin.message_user(request, 'Action update_entry_bucket_rules expects a visit model. Got %s' % (qs,))
            break
update_entry_bucket_rules.short_description = "Update entry bucket rules"
  
