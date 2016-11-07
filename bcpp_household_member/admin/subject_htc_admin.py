from django.contrib import admin

from ..admin_site import bcpp_household_member_admin
from ..models import SubjectHtc

from ..forms import SubjectHtcForm

from .modeladmin_mixins import HouseholdMemberAdminMixin


@admin.register(SubjectHtc, site=bcpp_household_member_admin)
class SubjectHtcAdmin(HouseholdMemberAdminMixin, admin.ModelAdmin):
    form = SubjectHtcForm
    dashboard_type = 'subject'
    subject_identifier_attribute = 'registration_identifier'
    fields = (
        'household_member',
        'report_datetime',
        'tracking_identifier',
        'offered',
        'accepted',
        'refusal_reason',
        'referred',
        'referral_clinic',
        'comment')

    radio_fields = {
        "offered": admin.VERTICAL,
        "accepted": admin.VERTICAL,
        "referred": admin.VERTICAL,
    }

    list_display = ('household_member', 'tracking_identifier', 'report_datetime', 'offered', 'accepted', 'referred')

    search_fields = [
        'tracking_identifier',
        'household_member__first_name',
        'household_member__household_structure__household__household_identifier']

    list_filter = ('report_datetime', 'offered', 'accepted', 'referred',
                   'household_member__household_structure__household__community')

    def get_readonly_fields(self, request, obj=None):
        super(SubjectHtcAdmin, self).get_readonly_fields(request, obj)
        return ('tracking_identifier',)
