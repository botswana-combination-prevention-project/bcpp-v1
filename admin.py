from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from django.db.models import Max
from bhp_registration.models import RegisteredSubject
from bhp_appointment.models import Appointment
from bhp_appointment.forms import AppointmentForm


class AppointmentAdmin(MyModelAdmin):

    form = AppointmentForm
    
    def save_model(self, request, obj, form, change):

        if change:
            obj.user_modified = request.user
        if not change:
            obj.user_created = request.user
            #set the visit instance
            aggr = Appointment.objects.filter(registered_subject=obj.registered_subject,visit_definition=obj.visit_definition).aggregate(Max('visit_instance'))
            if aggr['visit_instance__max'] <> None:
                obj.visit_instance = str(int(aggr['visit_instance__max']+1))
            else:
                obj.visit_instance = '0'
                
        return super(AppointmentAdmin, self).save_model(request, obj, form, change)                
                            
    #override, to check if non-default redirect 
    def add_view(self, request, form_url='', extra_context=None):

        result = super(AppointmentAdmin, self).add_view(request, form_url, extra_context)

        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
            if request.GET.get('next'):
                try:
                    # request.GET is an QueryDict. It is immutable so build a new dict. 
                    kwargs={}
                    # Just copying (.copy()) won't work cause i cannot pass kwarg 'next' to reverse
                    for k in request.GET.iterkeys():
                        # QueryDict where values are in a list per key, value has to be unicode. Convert list value to unicode                
                        kwargs[str(k)]=''.join(unicode(i) for i in request.GET.get(k))
                    # delete the 'next' key/value    
                    del kwargs['next']
                    result['Location'] = reverse(request.GET.get('next'),kwargs=kwargs )
                except:
                    pass                    
        return result   
                
    #override, to check if non-default redirect 
    def change_view(self, request, object_id, extra_context=None):

        result = super(AppointmentAdmin, self).change_view(request, object_id, extra_context)

        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
            if request.GET.get('next'):
                try:
                    # request.GET is an QueryDict. It is immutable so build a new dict. 
                    kwargs={}
                    # Just copying (.copy()) won't work cause i cannot pass kwarg 'next' to reverse
                    for k in request.GET.iterkeys():
                        # QueryDict where values are in a list per key, value has to be unicode. Convert list value to unicode                
                        kwargs[str(k)]=''.join(unicode(i) for i in request.GET.get(k))
                    # delete the 'next' key/value    
                    del kwargs['next']
                    result['Location'] = reverse(request.GET.get('next'),kwargs=kwargs )
                except:
                    pass                    
        return result  

    #override, limit dropdown in add_view to id passed in the URL        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('registered_subject'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(pk = request.GET.get('registered_subject'))
            else:
                kwargs["queryset"] = RegisteredSubject.objects.none()
        return super(AppointmentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)   



        
    fields = (
        'registered_subject',
        'appt_datetime',
        'appt_status',
        'visit_definition',        
        'visit_instance',
    )
    
    search_fields = ('registered_subject__subject_identifier',)
    
    list_display = (
        'registered_subject',
        'appt_datetime',
        'appt_status',
        'visit_definition',        
        'visit_instance',        
        )
    
    list_filter = (
        'appt_datetime',
        'appt_status',
        'visit_definition',        
        )
admin.site.register(Appointment, AppointmentAdmin)
