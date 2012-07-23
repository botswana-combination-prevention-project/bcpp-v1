from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyTabularInline
from django.db.models import Max

from bhp_registration.models import RegisteredSubject
from bhp_appointment.models import Appointment, Holiday, Configuration
from bhp_appointment.forms import AppointmentForm


class HolidayAdmin(MyModelAdmin):
    pass
admin.site.register(Holiday, HolidayAdmin)


class HolidayInlineAdmin(MyTabularInline):
    model = Holiday
    extra = 0


class ConfigurationAdmin(MyModelAdmin):
    inlines = [HolidayInlineAdmin, ]
admin.site.register(Configuration, ConfigurationAdmin)


class AppointmentAdmin(MyModelAdmin):

    form = AppointmentForm

    def save_model(self, request, obj, form, change):

        if change:
            obj.user_modified = request.user
        if not change:
            obj.user_created = request.user
            #set the visit instance
            aggr = Appointment.objects.filter(registered_subject=obj.registered_subject,
                                              visit_definition=obj.visit_definition).aggregate(Max('visit_instance'))
            if aggr['visit_instance__max'] is not None:
                obj.visit_instance = str(int(aggr['visit_instance__max'] + 1))
            else:
                obj.visit_instance = '0'
        return super(AppointmentAdmin, self).save_model(request, obj, form, change)

    #override, limit dropdown in add_view to id passed in the URL
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('registered_subject'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(pk=request.GET.get('registered_subject'))
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

    search_fields = ('registered_subject__subject_identifier', 'id')

    list_display = (
        'registered_subject',
        'appt_datetime',
        'appt_status',
        'visit_definition',
        'visit_instance',
        'created',
        'hostname_created',
        )

    list_filter = (
        'registered_subject__subject_type',
        'registered_subject__study_site__site_code',
        'appt_datetime',
        'appt_status',
        'visit_instance',
        'visit_definition',
        'created',
        'hostname_created',
        )

    radio_fields = {
        "appt_status": admin.VERTICAL,
        }

admin.site.register(Appointment, AppointmentAdmin)
