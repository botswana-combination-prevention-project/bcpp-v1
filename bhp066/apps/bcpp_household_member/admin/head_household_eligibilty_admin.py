from django.db.models import Q
from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from bhp066.apps.bcpp_household.models import HouseholdStructure

from ..models import HouseholdHeadEligibility, HouseholdMember
from ..forms import HouseholdHeadEligibilityForm
from bhp066.apps.bcpp_household_member.constants import HEAD_OF_HOUSEHOLD


class HouseholdHeadEligibilityAdmin(BaseModelAdmin):

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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            if request.GET.get('household_member'):
                kwargs["queryset"] = HouseholdMember.objects.filter(
                    Q(household_structure__exact=request.GET.get('household_structure', 0)),
                    (Q(is_consented=True) | Q(age_in_years__gte=18) | Q(relation=HEAD_OF_HOUSEHOLD)) &
                    (~Q(survival_status='Dead')))
            else:
                self.readonly_fields = list(self.readonly_fields)
                try:
                    self.readonly_fields.index('household_member')
                except ValueError:
                    self.readonly_fields.append('household_member')
        if db_field.name == "household_structure":
            if request.GET.get('household_structure'):
                kwargs["queryset"] = HouseholdStructure.objects.filter(
                    id__exact=request.GET.get('household_structure', 0))
            else:
                self.readonly_fields = list(self.readonly_fields)
                try:
                    self.readonly_fields.index('household_structure')
                except ValueError:
                    self.readonly_fields.append('household_structure')
        return super(HouseholdHeadEligibilityAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(HouseholdHeadEligibility, HouseholdHeadEligibilityAdmin)
