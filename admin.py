from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin, BaseTabularInline
from bhp_registration.models import RegisteredSubject
from bhp_appointment.models import Appointment
from forms import ScheduledEntryBucketForm
from bhp_entry.models import Entry, ScheduledEntryBucket, AdditionalEntryBucket


class EntryAdmin(BaseModelAdmin):

    search_fields = ('visit_definition__code', 'content_type_map__model', 'id')
    list_display = ('content_type_map', 'visit_definition', 'entry_order', 'required', 'entry_category')
    list_filter = ('entry_category', 'visit_definition__code', 'default_entry_status', 'created', 'content_type_map__model',)
admin.site.register(Entry, EntryAdmin)


class ScheduledEntryBucketAdmin(BaseModelAdmin):

    form = ScheduledEntryBucketForm
    search_fields = ('registered_subject__subject_identifier', 'entry__visit_definition__code', 'entry__content_type_map__model', 'id')
    list_display = ('registered_subject', 'entry', 'entry_status', 'fill_datetime', 'due_datetime', 'close_datetime', 'created', 'hostname_created')
    list_filter = ('entry_status', 'entry__visit_definition__code', 'fill_datetime', 'created', 'hostname_created')

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
        if db_field.name == "entry":
            if request.GET.get('visit_code'):
                kwargs["queryset"] = Entry.objects.filter(
                                                visit_definition__code=request.GET.get('visit_code'),
                                                content_type_map__model=request.GET.get('content_type_map'),
                                                )
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
        'upper_window_unit')
