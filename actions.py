from bhp_bucket.classes import bucket
from models import BaseVisitTracking

def update_entry_bucket_rules(modeladmin, request, queryset):
    for qs in queryset:
        if isinstance(qs, BaseVisitTracking):
            #ScheduledEntryBucket.objects.add_for_visit(visit_model_instance=qs)
            bucket.update_all(qs) 
        else:
            modeladmin.message_user(request, 'Action update_entry_bucket_rules expects a visit model. Got %s' % (qs,))
            break
update_entry_bucket_rules.short_description = "Update entry bucket rules"