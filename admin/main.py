from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin, BaseTabularInline
from bhp_registration.models import RegisteredSubject
from bhp_appointment.models import Appointment
from bhp_entry.forms import ScheduledEntryBucketForm
from bhp_entry.models import Entry, ScheduledEntryBucket, AdditionalEntryBucket


class EntryAdmin(BaseModelAdmin):

    search_fields = ('visit_definition__code', 'content_type_map__model', 'id')
    list_display = ('content_type_map', 'visit_definition', 'entry_order', 'required', 'entry_category', 'group_title')
    list_filter = ('entry_category', 'group_title', 'visit_definition__code', 'default_entry_status', 'created', 'content_type_map__model',)
admin.site.register(Entry, EntryAdmin)


class ScheduledEntryBucketAdmin(BaseModelAdmin):

    form = ScheduledEntryBucketForm
    search_fields = ('registered_subject__subject_identifier', 'entry__visit_definition__code', 'entry__content_type_map__model', 'id')
    list_display = ('registered_subject', 'entry', 'entry_status', 'fill_datetime', 'due_datetime', 'close_datetime', 'created', 'hostname_created')
    list_filter = ('entry_status', 'entry__visit_definition__code', 'fill_datetime', 'created', 'hostname_created')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            kwargs["queryset"] = RegisteredSubject.objects.filter(pk=request.GET.get('registered_subject'))
        if db_field.name == "appointment":
            kwargs["queryset"] = Appointment.objects.filter(pk=request.GET.get('appointment'))
        if db_field.name == "entry":
            kwargs["queryset"] = Entry.objects.filter(pk=request.GET.get('entry'))
        return super(ScheduledEntryBucketAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(ScheduledEntryBucket, ScheduledEntryBucketAdmin)


class AdditionalEntryBucketAdmin(BaseModelAdmin):
    list_display = ('registered_subject', 'content_type_map', 'entry_status', 'fill_datetime', 'due_datetime', 'close_datetime', 'rule_name')
    list_filter = ('entry_status', 'fill_datetime', 'rule_name')
    search_fields = ('registered_subject__subject_identifier', 'content_type_map__model', 'id', 'rule_name')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('subject_identifier'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(subject_identifier=request.GET.get('subject_identifier'))
        return super(AdditionalEntryBucketAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(AdditionalEntryBucket, AdditionalEntryBucketAdmin)


class EntryInline (BaseTabularInline):
    model = Entry
    extra = 0
    fields = (
        'content_type_map',
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
        'group_title')
