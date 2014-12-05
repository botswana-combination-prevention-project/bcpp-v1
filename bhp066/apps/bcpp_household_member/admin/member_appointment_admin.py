from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..forms import MemberAppointmentForm
from ..models import MemberAppointment


class MemberAppointmentAdmin(BaseModelAdmin):

    form = MemberAppointmentForm

    list_display = (
        'household_member',
        'survey',
        'label',
        'composition',
        'call_list',
        'work_list',
        'appt_date',
        'appt_status'
        )

    list_filter = (
        'survey',
        'label',
        'appt_date',
        'appt_status'
        )

    readonly_fields = ("household_member", 'survey')

    search_fields = (
        'household_member__first_name',
        'household_member__household_structure__pk',
        'household_member__household_structure__household__household_identifier',
        'household_member__household_structure__household__plot__plot_identifier',
        )

admin.site.register(MemberAppointment, MemberAppointmentAdmin)
