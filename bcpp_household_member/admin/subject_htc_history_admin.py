from django.contrib import admin

from ..admin_site import bcpp_household_member_admin
from ..models import SubjectHtcHistory

from .modeladmin_mixins import HouseholdMemberAdminMixin


@admin.register(SubjectHtcHistory, site=bcpp_household_member_admin)
class SubjectHtcHistoryAdmin(HouseholdMemberAdminMixin, admin.ModelAdmin):

    fields = (
        'household_member',
        'report_datetime',
        'offered',
        'accepted',
        'refusal_reason',
        'tracking_identifier',
        'referred',
        'referral_clinic')

    radio_fields = {"offered": admin.VERTICAL,
                    "accepted": admin.VERTICAL,
                    "referred": admin.VERTICAL}

    list_display = ('household_member', 'report_datetime', 'tracking_identifier')

    search_fields = [
        'household_member__first_name',
        'household_member__household_structure__household__household_identifier',
        'tracking_identifier']

    list_filter = ('household_member__household_structure__household__community',
                   'report_datetime', 'offered', 'accepted', 'referred', 'referral_clinic')

    instructions = []
