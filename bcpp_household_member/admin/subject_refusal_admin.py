from django.contrib import admin

from ..admin_site import bcpp_household_member_admin
from ..forms import SubjectRefusalForm
from ..models import SubjectRefusal

from .modeladmin_mixins import HouseholdMemberAdminMixin


@admin.register(SubjectRefusal, site=bcpp_household_member_admin)
class SubjectRefusalAdmin(HouseholdMemberAdminMixin, admin.ModelAdmin):
    form = SubjectRefusalForm
    dashboard_type = 'subject'
    subject_identifier_attribute = 'registration_identifier'
    fields = (
        'household_member',
        'report_datetime',
        'refusal_date',
        'reason',
        'reason_other',
        'comment')

    radio_fields = {"reason": admin.VERTICAL}

    list_display = ('reason', )

    search_fields = [
        'household_member__first_name',
        'household_member__household_structure__household__household_identifier']

    list_filter = ('reason', 'household_member__household_structure__household__community')
