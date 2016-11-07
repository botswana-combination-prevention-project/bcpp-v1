from django.contrib import admin

from ..admin_site import bcpp_household_member_admin
from ..forms import MemberAppointmentForm
from ..models import MemberAppointment

from .modeladmin_mixins import HouseholdMemberAdminMixin


@admin.register(MemberAppointment, site=bcpp_household_member_admin)
class MemberAppointmentAdmin(HouseholdMemberAdminMixin, admin.ModelAdmin):

    form = MemberAppointmentForm

    date_hierarchy = 'appt_date'

    list_display = (
        'household_member',
        'survey',
        'label',
        'composition',
        'call_list',
        'work_list',
        'appt_date',
        'appt_status',
        'user_created',
        'user_modified',
    )

    list_filter = (
        'survey',
        'label',
        'appt_date',
        'appt_status',
        'user_created',
        'user_modified',
        'hostname_created',
        'hostname_modified',
    )

    readonly_fields = ("household_member", 'survey')

    search_fields = (
        'household_member__first_name',
        'household_member__household_structure__pk',
        'household_member__household_structure__household__household_identifier',
        'household_member__household_structure__household__plot__plot_identifier',
    )
