from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from django.db.models import Max
from django.contrib import messages
from bhp_visit.classes import WindowPeriod
from bhp_registration.models import RegisteredSubject
from bhp_appointment.models import Appointment
from bhp_appointment.forms import AppointmentForm
from pre_appointment_contact_admin import PreAppointmentContactInlineAdmin


class AppointmentAdmin(BaseModelAdmin):

    """ModelAdmin class to handle appointments."""

    form = AppointmentForm
    date_hierarchy = 'appt_datetime'
    inlines = [PreAppointmentContactInlineAdmin, ]

#     def save_model(self, request, obj, form, change):
#         """Saves an appointment if handled through admin.
# 
#             1. On change, checks the window period using :class:`bhp_visit.classes.WindowPeriod` and warns if out.
#             2. If new, sets the visit 'instance' to '0' or one plus the max.
#         """
#         if change:
#             obj.user_modified = request.user
#             window_period = WindowPeriod()
#             if not window_period.check_datetime(obj.visit_definition, obj.appt_datetime, obj.best_appt_datetime):
#                 messages.add_message(request, messages.ERROR, window_period.error_message)
# 
#         if not change:
#             obj.user_created = request.user
#             #set the visit instance
#             aggr = Appointment.objects.filter(registered_subject=obj.registered_subject,
#                                               visit_definition=obj.visit_definition).aggregate(Max('visit_instance'))
#             if aggr['visit_instance__max'] is not None:
#                 obj.visit_instance = str(int(aggr['visit_instance__max'] + 1))
#             else:
#                 obj.visit_instance = '0'
#         return super(AppointmentAdmin, self).save_model(request, obj, form, change)

    #override, limit dropdown in add_view to id passed in the URL
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limits the dropdown for 'registered_subject'"""
        if db_field.name == "registered_subject":
            if request.GET.get('registered_subject'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(pk=request.GET.get('registered_subject'))
            #else:
            #    kwargs["queryset"] = RegisteredSubject.objects.none()
        return super(AppointmentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    fields = (
        'registered_subject',
        'appt_datetime',
        'appt_status',
        'study_site',
        'visit_definition',
        'visit_instance',
        'appt_type',
    )

    search_fields = ('registered_subject__subject_identifier', 'id')

    list_display = (
        'registered_subject',
        'dashboard',
        'appt_datetime',
        'appt_type',
        'appt_status',
        'is_confirmed',
        'contact_count',
        'visit_definition',
        'visit_instance',
        'best_appt_datetime',
        'created',
        'hostname_created',
        )

    list_filter = (
        'study_site',
        'registered_subject__subject_type',
        'appt_type',
        'is_confirmed',
        'contact_count',
        'appt_datetime',
        'appt_status',
        'visit_instance',
        'visit_definition',
        'created',
        'user_created',
        'hostname_created',
        )

    radio_fields = {
        "appt_status": admin.VERTICAL,
        'study_site': admin.VERTICAL,
        'appt_type': admin.VERTICAL,
        }

admin.site.register(Appointment, AppointmentAdmin)
