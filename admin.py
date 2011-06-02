from datetime import datetime, date
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Avg, Max, Min, Count
from bhp_common.models import MyModelAdmin, MyStackedInline
from bhp_form.models import Entry, EntryBucket
from bhp_visit.models import Appointment, VisitDefinition, VisitTrackingSubjCurrStatus, VisitTrackingInfoSource, VisitTrackingVisitReason, ScheduleGroup
from forms import AppointmentForm

class ScheduleGroupAdmin(MyModelAdmin):
    list_display = ('group_name', 'membership_form', 'grouping_key')
admin.site.register(ScheduleGroup, ScheduleGroupAdmin)    

class EntryInline (admin.TabularInline):
    model = Entry
    extra =0
    fields = (
        'entry_form',
        'entry_order',
        'required',
        'entry_category',
        'entry_window_calculation',
        'time_point',
        'lower_window',
        'lower_window_unit',
        'upper_window',
        'upper_window_unit',
    )
    


#VisitTrackingReport
class VisitDefinitionAdmin(MyModelAdmin):
    list_display = ('code', 'title', 'time_point', 'lower_window', 'lower_window_unit', 'upper_window', 'upper_window_unit')
    
    inlines = [EntryInline,]
        
admin.site.register(VisitDefinition, VisitDefinitionAdmin)

admin.site.register(VisitTrackingInfoSource)
admin.site.register(VisitTrackingVisitReason)
admin.site.register(VisitTrackingSubjCurrStatus)


"""
class VisitTrackingReportAdmin(MyModelAdmin):
    fields = (
        'registered_subject',
        'appointment',
        'visit_datetime',
        'subject_current_status',
        'info_source',
        'info_source_other',        
        'visit_reason',
        'visit_reason_missed',        
        'next_scheduled_visit_datetime',
    )
admin.site.register(VisitTrackingReport, VisitTrackingReportAdmin)
"""

class AppointmentAdmin(MyModelAdmin):

    form = AppointmentForm
    def save_model(self, request, obj, form, change):

        if change:
            obj.user_modified = request.user
            obj.save()        
            
        if not change:
            obj.user_created = request.user
            
            #set the visit instance
            aggr = Appointment.objects.filter(registered_subject=obj.registered_subject,visit_definition=obj.visit_definition).aggregate(Max('visit_instance'))
            if aggr['visit_instance__max']:
                obj.visit_instance = aggr['visit_instance__max']+1
            else:
                obj.visit_instance = 0
            obj.save()
                            
            #fill the entry bucket for this visit
            if obj.visit_instance == 0:
                filled_datetime = datetime.today()
                oEntry = Entry.objects.filter(visit_definition=obj.visit_definition)
                
                #due_datetime = obj.visit_definition.get_lower_window_datetime(obj.appt_datetime)
                
                for entry in oEntry:
                    oEntryBucket=EntryBucket(
                        registered_subject=obj.registered_subject,
                        appointment = obj,
                        entry = entry,
                        current_entry_title = entry.entry_form.model_class()._meta.verbose_name,
                        #entry_url = entry.entry_form.model_class().get_absolute_url(),
                        fill_datetime = filled_datetime,
                        due_datetime = entry.visit_definition.get_upper_window_datetime(obj.appt_datetime),                      
                        )
                    oEntryBucket.save()             

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
        
    fields = (
        'registered_subject',
        'appt_datetime',
        'appt_status',
        'visit_definition',        
        'visit_instance',
    )
admin.site.register(Appointment, AppointmentAdmin)

