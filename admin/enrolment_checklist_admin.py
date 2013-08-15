from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bcpp_household.models import HouseholdStructure
from bcpp_household_member.models import EnrolmentChecklist, HouseholdMember
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
        "citizen",
        "legal_marriage",
        "marriage_certificate",
        "marriage_certificate_no",
        "community_resident")

    list_display = (
        'household_member',
        'composition',
        "report_datetime",
        'eligible',
        )

    list_filter = [
        'eligible',
        "report_datetime",
        ]

    radio_fields = {
        "is_dob_estimated": admin.VERTICAL,
        "gender": admin.VERTICAL,
        "citizen": admin.VERTICAL,
        "legal_marriage": admin.VERTICAL,
        "marriage_certificate": admin.VERTICAL,
        "community_resident": admin.VERTICAL, }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_structure":
            kwargs["queryset"] = HouseholdStructure.objects.filter(id__exact=request.GET.get('household_structure', 0))
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(EnrolmentChecklistAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(EnrolmentChecklist, EnrolmentChecklistAdmin)
