from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from bhp_visit.models import RegisteredSubjectAppointment, VisitDefinition, VisitTrackingSubjCurrStatus, VisitTrackingInfoSource, VisitTrackingVisitReason
#VisitTrackingReport

admin.site.register(VisitDefinition)
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
    fields = (
        'registered_subject',
        'appt_datetime',
        'appt_status',
        'visit_definition',        
        'visit_instance',
    )
admin.site.register(RegisteredSubjectAppointment, AppointmentAdmin)

