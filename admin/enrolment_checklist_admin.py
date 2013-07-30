from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bcpp_household.models import HouseholdStructure
from bcpp_household_member.models import EnrolmentChecklist
from bcpp_household_member.forms import EnrolmentChecklistForm


class EnrolmentChecklistAdmin(BaseModelAdmin):

    form = EnrolmentChecklistForm
    fields = (
        'household_member',
        "report_datetime",
        'dob',
        'is_dob_estimated',
        'gender',
        'omang',
        "mental_capacity",
        "incarceration",
        "citizen",
        "community_resident")

    radio_fields = {
        "mental_capacity": admin.VERTICAL,
        "incarceration": admin.VERTICAL,
        "citizen": admin.VERTICAL,
        "community_resident": admin.VERTICAL, }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_structure":
            kwargs["queryset"] = HouseholdStructure.objects.filter(id__exact=request.GET.get('household_structure', 0))

        return super(EnrolmentChecklistAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(EnrolmentChecklist, EnrolmentChecklistAdmin)
