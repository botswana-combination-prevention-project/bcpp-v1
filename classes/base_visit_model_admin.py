from django.db.models import Q, ForeignKey
from django.core.urlresolvers import reverse
from bhp_common.models import MyModelAdmin
from bhp_entry.models import ScheduledEntryBucket


class BaseVisitModelAdmin(MyModelAdmin):

    """ModelAdmin subclass for models with a ForeignKey to 'visit'
    
    Takes care of updating the bucket and redirecting back to the dashboard after
    delete()
    
    """ 

    def __init__(self, *args, **kwargs):
        
        super(BaseVisitModelAdmin, self).__init__(*args, **kwargs)

    def save_model(self, request, obj, form, change):

        ScheduledEntryBucket.objects.update_status(
            model = obj,
            visit_model = self.visit_model,
            )
                        
        return super(BaseVisitModelAdmin, self).save_model(request, obj, form, change)
        
    def delete_model(self, request, obj):

        ScheduledEntryBucket.objects.update_status(
            model = obj,
            visit_model = self.visit_model,
            action = 'delete',
            )
            
        return super(BaseVisitModelAdmin, self).delete_model(request, obj) 

    def delete_view(self, request, object_id, extra_context=None):

        """ delete requires knowledge of the model which is not given, so get it from the form.__dict__ and reverse resolve"""

        # get visit foreignkey field name
        visit_fk_name = [fk for fk in [f for f in self.model._meta.fields if isinstance(f,ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name][0].name        
        
        subject_identifier = self.form.__dict__['base_fields'][visit_fk_name].__dict__['_queryset'][0].appointment.registered_subject.subject_identifier
        visit_code = self.form.__dict__['base_fields'][visit_fk_name].__dict__['_queryset'][0].appointment.visit_definition.code

        result = super(BaseVisitModelAdmin, self).delete_view(request, object_id, extra_context)
        result['Location'] = reverse('dashboard_visit_url' , kwargs={'dashboard_type':'subject', 'subject_identifier':subject_identifier, 'visit_code': unicode(visit_code)})

        return result
        
    #override, limit dropdown in add_view to id passed in the URL        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        visit_fk = [fk for fk in [f for f in self.model._meta.fields if isinstance(f,ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name]        
        if db_field.name == visit_fk[0].name:
            kwargs["queryset"] = self.visit_model.objects.filter(appointment__registered_subject__subject_identifier=request.GET.get('subject_identifier', 0), 
                                                        appointment__visit_definition__code=request.GET.get('visit_code', 0),
                                                        appointment__visit_instance=request.GET.get('visit_instance', 0),
                                                        )                                                        
        return super(BaseVisitModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)   

