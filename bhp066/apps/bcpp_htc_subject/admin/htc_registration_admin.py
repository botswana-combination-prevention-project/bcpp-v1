from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp066.apps.bcpp_household.models import HouseholdStructure
from bhp066.apps.bcpp_household_member.models import HouseholdMember
from ..models import HtcRegistration
from ..forms import HtcRegistrationForm


class HtcRegistrationAdmin(BaseModelAdmin):

    form = HtcRegistrationForm
    fields = (
        'household_member',
        "report_datetime",
        "is_resident",
        "your_community",
        "citizen",
        'omang',
        'dob',
        'is_dob_estimated',
        'gender',
        "is_pregnant",
        "testing_counseling_site",
    )

    list_display = (
        'household_member',
        "report_datetime",
    )

    list_filter = ["report_datetime"]

    radio_fields = {
        "is_resident": admin.VERTICAL,
        "your_community": admin.VERTICAL,
        "is_dob_estimated": admin.VERTICAL,
        "gender": admin.VERTICAL,
        "citizen": admin.VERTICAL,
        "is_pregnant": admin.VERTICAL,
        "testing_counseling_site": admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_structure":
            kwargs["queryset"] = HouseholdStructure.objects.filter(id__exact=request.GET.get('household_structure', 0))
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(HtcRegistrationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(HtcRegistration, HtcRegistrationAdmin)
