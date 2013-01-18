from django.contrib import admin
from bhp_common.models import MyModelAdmin
from bhp_registration.models import RegisteredSubject
from bhp_appointment.models import Appointment
from forms import ScheduledLabEntryBucketForm
from bhp_lab_entry.models import LabEntry, LabEntryUnscheduled, ScheduledLabEntryBucket, AdditionalLabEntryBucket


class LabEntryAdmin(MyModelAdmin):

    search_fields = ('visit_definition__code', 'panel__name', 'lab_clinic_api_panel')

    list_display = ('panel', 'lab_clinic_api_panel', 'visit_definition', 'entry_order', 'required', 'entry_category')

    list_filter = ('entry_category', 'visit_definition__code', 'default_entry_status', 'created', 'lab_clinic_api_panel', 'panel__name',)

admin.site.register(LabEntry, LabEntryAdmin)


class LabEntryUnscheduledAdmin(MyModelAdmin):

    search_fields = ('panel__name',)

    list_display = ('panel', 'entry_order', 'required', 'entry_category')

    list_filter = ('entry_category', 'default_entry_status', 'created', 'panel__name',)

admin.site.register(LabEntryUnscheduled, LabEntryUnscheduledAdmin)


class AdditionalLabEntryBucketAdmin(MyModelAdmin):
    pass
admin.site.register(AdditionalLabEntryBucket, AdditionalLabEntryBucketAdmin)


class ScheduledLabEntryBucketAdmin(MyModelAdmin):

    form = ScheduledLabEntryBucketForm

    search_fields = ('registered_subject__subject_identifier', 'lab_entry__visit_definition__code', 'lab_entry__panel__name')

    list_display = ('registered_subject', 'lab_entry', 'entry_status', 'fill_datetime', 'due_datetime', 'close_datetime')

    list_filter = ('entry_status', 'lab_entry__visit_definition__code', 'fill_datetime',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "registered_subject":
            if request.GET.get('subject_identifier'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(subject_identifier=request.GET.get('subject_identifier'))
        if db_field.name == "appointment":
            if request.GET.get('subject_identifier'):
                kwargs["queryset"] = Appointment.objects.filter(
                                                registered_subject__subject_identifier=request.GET.get('subject_identifier'),
                                                visit_definition__code=request.GET.get('visit_code'),
                                                visit_instance=request.GET.get('visit_instance'),
                                                )
        if db_field.name == "lab_entry":
            if request.GET.get('visit_code'):
                kwargs["queryset"] = LabEntry.objects.filter(
                                                visit_definition__code=request.GET.get('visit_code'),
                                                panel=request.GET.get('panel'),
                                                )
        return super(ScheduledLabEntryBucketAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(ScheduledLabEntryBucket, ScheduledLabEntryBucketAdmin)


class LabEntryInline (admin.TabularInline):
    model = LabEntry
    extra = 0
    fields = (
        'panel',
        'entry_order',
        'required',
        'default_entry_status',
        'entry_category',
        'entry_window_calculation',
        'time_point',
        'lower_window',
        'lower_window_unit',
        'upper_window',
        'upper_window_unit',

    )
