from django.contrib import admin

from ..admin_site import bcpp_household_member_admin
from ..models import SubjectRefusalHistory

from .modeladmin_mixins import HouseholdMemberAdminMixin


@admin.register(SubjectRefusalHistory, site=bcpp_household_member_admin)
class SubjectRefusalHistoryAdmin(HouseholdMemberAdminMixin, admin.ModelAdmin):

    fields = (
        'household_member',
        'report_datetime',
        'refusal_date',
        'reason',
        'reason_other')

    radio_fields = {"reason": admin.VERTICAL}

    list_display = ('household_member', 'report_datetime', )

    search_fields = [
        'household_member__first_name',
        'household_member__household_structure__household__household_identifier']

    list_filter = ('reason', 'household_member__household_structure__household__community')

    instructions = []
