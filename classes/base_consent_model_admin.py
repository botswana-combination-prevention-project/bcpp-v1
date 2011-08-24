from django.core.urlresolvers import reverse
from django.db.models import ForeignKey
from bhp_common.models import MyModelAdmin
from bhp_registration.models import RegisteredSubject

class BaseConsentModelAdmin(MyModelAdmin):

    def save_model(self, request, obj, form, change):
        
        if not change:
            
            consent_fk_name = [fk for fk in [f for f in self.model._meta.fields if isinstance(f,ForeignKey)] if fk.rel.to._meta.module_name == self.consent_model._meta.module_name][0].name        
            subject_identifier = self.form.__dict__['base_fields'][consent_fk_name].__dict__['_queryset'][0].registered_subject.subject_identifier

            rs = RegisteredSubject.objects.get(subject_identifier = subject_identifier)
            obj.registered_subject = rs

            #if model is in a member of a schedule group, create appointments
            Appointment.objects.create_appointments( 
                registered_subject = obj.registered_subject, 
                base_appt_datetime = datetime.today(), 
                model_name = self.form._meta.model.__name__.lower(),
                )

        return super(BaseConsentModelAdmin, self).save_model(request, obj, form, change)                        

    def add_view(self, request, form_url='', extra_context=None):
        
        result = super(BaseConsentModelAdmin, self).add_view(request, form_url, extra_context)

        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
            if request.GET.get('next'):
                url_parameters = { 'subject_identifier':request.GET.get('subject_identifier'), 'dashboard_type':request.GET.get('dashboard_type'),}
                result['Location'] = reverse(request.GET.get('next'), kwargs=url_parameters)
        return result                     
        
    def change_view(self, request, object_id, extra_context=None):

        result = super(BaseConsentModelAdmin, self).change_view(request, object_id, extra_context)
        
        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
            if request.GET.get('next'):
                url_parameters = { 'subject_identifier':request.GET.get('subject_identifier'), 'dashboard_type':request.GET.get('dashboard_type'),}
                result['Location'] = reverse(request.GET.get('next'), kwargs=url_parameters)

        return result     

    #override, limit dropdown in add_view to id passed in the URL        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        consent_fk_name = [fk for fk in [f for f in self.model._meta.fields if isinstance(f,ForeignKey)] if fk.rel.to._meta.module_name == self.consent_model._meta.module_name][0].name        
        if request.GET.get('subject_identifier'):
            if db_field.name == consent_fk_name:
                kwargs["queryset"] = self.consent_model.objects.filter(subject_identifier=request.GET.get('subject_identifier'))                                                        
        return super(BaseConsentModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)   



    #override to disallow subject to be changed
    def get_readonly_fields(self, request, obj = None):

        consent_fk_name = [fk for fk in [f for f in self.model._meta.fields if isinstance(f,ForeignKey)] if fk.rel.to._meta.module_name == self.consent_model._meta.module_name][0].name        

        if obj: #In edit mode
            return (consent_fk_name,'registration_datetime') + self.readonly_fields
        else:
            return self.readonly_fields  

