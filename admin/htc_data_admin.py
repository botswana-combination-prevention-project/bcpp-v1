from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bcpp_household.models import HouseholdStructure
from bcpp_household_member.models import HtcData, HouseholdMember
from bcpp_household_member.forms import HtcDataForm


class HtcDataAdmin(BaseModelAdmin):

    form = HtcDataForm
    fields = (
        'household_member',
        "report_datetime",
        'dob',
        'is_dob_estimated',
        'gender',
        'omang',
        "citizen",
        'rel',
        'rel_other',
        'ethnic',
        'other',
        'marital_status',
        'num_wives',
        'husband_wives',
        'hiv_result',
        'why_not_tested',)

    list_display = (
        'household_member',
#         'composition',
        "report_datetime",
        )

    list_filter = ["report_datetime",]

    radio_fields = {
        "is_dob_estimated": admin.VERTICAL,
        "gender": admin.VERTICAL,
        "citizen": admin.VERTICAL,
        "marital_status": admin.VERTICAL, 
        "hiv_result": admin.VERTICAL,
        "why_not_tested": admin.VERTICAL,}
    
    filter_horizontal = ('rel',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_structure":
            kwargs["queryset"] = HouseholdStructure.objects.filter(id__exact=request.GET.get('household_structure', 0))
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(HtcDataAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(HtcData, HtcDataAdmin)
