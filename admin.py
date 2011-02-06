from django.contrib import admin
from bhp_admin_models.models import MyModelAdmin, MyStackedInline
from models import Appointment, VisitDefinition, VisitTrackingInfoSource, VisitTrackingVisitReason, VisitReport

admin.site.register(VisitDefinition)
admin.site.register(VisitTrackingInfoSource)
admin.site.register(VisitTrackingVisitReason)


class VisitReportAdmin(MyModelAdmin):
    fields = (
        'appointment',
        'visit_datetime',
        'info_source',
        'info_source_other',        
        'visit_reason',
        'visit_reason_missed',        
        'next_scheduled_visit_datetime',
    )
admin.site.register(VisitReport, VisitReportAdmin)

class AppointmentAdmin(MyModelAdmin):
    fields = (
        'subject_identifier',
        'appt_datetime',
        'appt_status',
        'visit_definition',        
        'visit_instance',
    )
admin.site.register(Appointment, AppointmentAdmin)

