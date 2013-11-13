from django.contrib import admin
from edc.base.admin.admin import BaseTabularInline, BaseModelAdmin
from edc.export.actions import export_as_csv_action
from apps.bcpp_household.models import HouseholdStructure
from ..models import HouseholdMember
from ..forms import HouseholdMemberForm


class HouseholdMemberInline(BaseTabularInline):
    model = HouseholdMember
    extra = 3


class HouseholdMemberAdmin(BaseModelAdmin):

    form = HouseholdMemberForm
    date_hierarchy = 'modified'
    actions = [export_as_csv_action("Export as csv", fields=['initials', 'gender', 'age_in_years', 'present_today', 'study_resident', 'relation',
                                                             'eligible_member',
                                                             'eligible_subject',
                                                             'member_status'], extra_fields={'plot_identifier': 'household_structure__household__plot__plot_identifier'})]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_structure":
            kwargs["queryset"] = HouseholdStructure.objects.filter(id__exact=request.GET.get('household_structure', 0))

        return super(HouseholdMemberAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    fields = ('household_structure', 'first_name', 'initials', 'gender', 'age_in_years', 'present_today', 'study_resident', 'relation')

    radio_fields = {
        "gender": admin.VERTICAL,
        "relation": admin.VERTICAL,
        "present_today": admin.VERTICAL,
        "study_resident": admin.VERTICAL,
        }

    list_display = ('first_name', 'initials',
                    'household_structure',
                    'to_locator',
                    'hiv_history',
                    'relation',
                    'eligible_member',
                    'eligible_subject',
                    'is_consented',
                    'member_status',
                    'created',
                    'hostname_created')

    search_fields = [
        'first_name',
        'household_structure__id',
        'household_structure__household__household_identifier',
        'household_structure__household__id',
        'household_structure__household__plot__plot_identifier',
        'household_structure__household__plot__id',
        'relation', 'id']

    list_filter = ('household_structure__survey__survey_name', 'present_today', 'study_resident', 'member_status',
                   'eligible_member', 'eligible_subject', 'target', 'hiv_history', 'household_structure__household__community',
                    'modified', 'hostname_created')
    list_per_page = 15
admin.site.register(HouseholdMember, HouseholdMemberAdmin)
