from django.contrib import admin

from ..admin_site import bcpp_household_member_admin
from ..models import HouseholdHeadEligibility
from ..forms import HouseholdHeadEligibilityForm

from .modeladmin_mixins import HouseholdMemberAdminMixin


@admin.register(HouseholdHeadEligibility, site=bcpp_household_member_admin)
class HouseholdHeadEligibilityAdmin(HouseholdMemberAdminMixin, admin.ModelAdmin):

    instructions = ['Important: The household member must verbally consent before completing this questionnaire.']

    form = HouseholdHeadEligibilityForm
    fields = (
        "household_structure",
        "household_member",
        "report_datetime",
        "aged_over_18",
        'household_residency',
        "verbal_script")

    radio_fields = {
        "aged_over_18": admin.VERTICAL,
        "household_residency": admin.VERTICAL,
        "verbal_script": admin.VERTICAL}

    list_filter = ('report_datetime', 'user_created', 'user_modified', 'hostname_created',
                   'household_member__household_structure__household__community')
