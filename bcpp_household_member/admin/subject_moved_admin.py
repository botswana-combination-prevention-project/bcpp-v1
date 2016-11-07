from django.contrib import admin

from ..admin_site import bcpp_household_member_admin
from ..forms import SubjectMovedForm
from ..models import SubjectMoved

from .modeladmin_mixins import HouseholdMemberAdminMixin


@admin.register(SubjectMoved, site=bcpp_household_member_admin)
class SubjectMovedAdmin(HouseholdMemberAdminMixin, admin.ModelAdmin):
    form = SubjectMovedForm
    dashboard_type = 'subject'
    subject_identifier_attribute = 'registration_identifier'

    fields = (
        'household_member',
        'report_datetime',
        'moved_household',
        'moved_community',
        'new_community',
        'update_locator',
        'comment')
    list_display = (
        'household_member',
        'moved_household',
        'moved_community',
        'new_community',
        'update_locator',
    )
    search_fields = [
        'household_member__first_name',
        'household_member__household_structure__household__household_identifier']
    list_filter = ('survey', 'household_member__household_structure__household__community')
    radio_fields = {
        "moved_household": admin.VERTICAL,
        "moved_community": admin.VERTICAL,
        "update_locator": admin.VERTICAL,
    }
