from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from bhp066.apps.bcpp_household_member.models import HouseholdMember

from ..actions import call_participant, update_call_list_action
from ..forms import CallListForm
from ..models import CallList


class CallListAdmin(BaseModelAdmin):

    form = CallListForm
    date_hierarchy = 'created'
    fields = (
        "household_member",
        "subject_identifier",
        'call_attempts',
        'label',
        'call_status',
        'call_outcome',
    )
    radio_fields = {'call_status': admin.VERTICAL}

    list_display = (
        "subject_identifier",
        'first_name',
        'initials',
        'gender',
        'age_in_years',
        'composition',
        'work_list',
        'appt',
        'community',
        'label',
        'call_attempts',
        'call_status',
        'call_outcome',
        'referral_code',
        "bhs",
        "hic",
        'created',
        "consent_datetime",
        'hostname_created',
        'user_created',
    )
    list_filter = (
        'community',
        'label',
        'call_attempts',
        'call_status',
        'created',
        'bhs',
        'hic',
        'gender',
        'consent_datetime',
        'referral_code',
        'hostname_created',
        'user_created',
    )

    readonly_fields = (
        "subject_identifier",
        'call_attempts',
        'household_member',
    )

    search_fields = ('subject_identifier',
                     'first_name',
                     'initials',
                     'household_member__household_structure__pk',
                     'household_member__household_structure__household__household_identifier')

    actions = [call_participant, update_call_list_action]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(CallListAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(CallList, CallListAdmin)
