from django.contrib import admin
from edc.base.admin.admin import BaseTabularInline, BaseModelAdmin
from edc.core.bhp_export_data.actions import export_as_csv_action
from apps.bcpp_household.models import HouseholdStructure
from ..models import HouseholdMember
from ..forms import HouseholdMemberForm


class HouseholdMemberInline(BaseTabularInline):
    model = HouseholdMember
    extra = 3


class HouseholdMemberAdmin(BaseModelAdmin):

    form = HouseholdMemberForm
    date_hierarchy = 'modified'
    actions = [export_as_csv_action("Export as csv", fields=[], exclude=['id', ])]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_structure":
            kwargs["queryset"] = HouseholdStructure.objects.filter(id__exact=request.GET.get('household_structure', 0))

        return super(HouseholdMemberAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    fields = ('household_structure', 'first_name', 'initials', 'gender', 'age_in_years', 'present', 'nights_out', 'relation', 'lives_in_household')

    radio_fields = {
        "gender": admin.VERTICAL,
        "relation": admin.VERTICAL,
        "present": admin.VERTICAL,
        "lives_in_household": admin.VERTICAL,
        }

    list_display = ('subject',
                    'household_structure',
                    'survey',
                    'to_locator',
                    'hiv_history',
                    'resident',
                    'relation',
                    'present',
                    'is_eligible_member',
                    'member_status',
                    'created',
                    'hostname_created')

    search_fields = [
        'first_name',
        'household_structure__id',
        'household_structure__household__household_identifier',
        'household_structure__household__id',
        'household_structure__plot__plot_identifier',
        'household_structure__plot__id',
        'relation', 'id']

    list_filter = ('survey__survey_name', "present", 'member_status', 'modified',
                   'is_eligible_member', 'target', 'hiv_history',
                   'hostname_created')
    list_per_page = 15
admin.site.register(HouseholdMember, HouseholdMemberAdmin)
