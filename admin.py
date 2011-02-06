from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from models import Appointment, VisitDefinition, VisitTrackingInfoSource, VisitTrackingVisitReason, VisitTrackingReport

admin.site.register(VisitDefinition)
admin.site.register(VisitTrackingInfoSource)
admin.site.register(VisitTrackingVisitReason)


class VisitTrackingReportAdmin(MyModelAdmin):
    fields = (
        'registered_subject',
        'appointment',
        'visit_datetime',
        'info_source',
        'info_source_other',        
        'visit_reason',
        'visit_reason_missed',        
        'next_scheduled_visit_datetime',
    )
admin.site.register(VisitTrackingReport, VisitTrackingReportAdmin)


class AppointmentAdmin(MyModelAdmin):
    fields = (
        'subject_consent',
        'appt_datetime',
        'appt_status',
        'visit_definition',        
        'visit_instance',
    )
admin.site.register(Appointment, AppointmentAdmin)

