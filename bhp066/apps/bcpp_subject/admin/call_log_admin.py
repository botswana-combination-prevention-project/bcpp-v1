from django.contrib import admin

from apps.bcpp_household_member.models import HouseholdMember

from ..forms import CallLogForm, CallLogEntryForm
from ..models import CallLog, CallLogEntry

from edc.base.modeladmin.admin import BaseModelAdmin


class CallLogAdmin(BaseModelAdmin):

    form = CallLogForm
    fields = ("household_member", )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(CallLogAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(CallLog, CallLogAdmin)


class CallLogEntryAdmin(BaseModelAdmin):

    form = CallLogEntryForm
    fields = (
        'call_log',
        'call_datetime',
        'contact_type',
        'has_moved_community',
        'new_community',
        'update_locator',
        'available',
        'time_of_week',
        'time_of_day',
        'appt',
        'appt_date',
        'appt_grading',
        'appt_location',
        'appt_location_other'
        )

    radio_fields = {
        "contact_type": admin.VERTICAL,
        "update_locator": admin.VERTICAL,
        "has_moved_community": admin.VERTICAL,
        "available": admin.VERTICAL,
        "time_of_week": admin.VERTICAL,
        "time_of_day": admin.VERTICAL,
        "appt": admin.VERTICAL,
        "appt_grading": admin.VERTICAL,
        "appt_location": admin.VERTICAL,
        }
    

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "call_log":
            kwargs["queryset"] = CallLog.objects.filter(id__exact=request.GET.get('call_log', 0))
        return super(CallLogEntryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(CallLogEntry, CallLogEntryAdmin)
