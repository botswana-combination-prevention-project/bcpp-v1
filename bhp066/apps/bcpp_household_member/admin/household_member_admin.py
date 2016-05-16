from django.contrib import admin

from edc_base.modeladmin.admin import BaseTabularInline
from edc.export.actions import export_as_csv_action

from bhp066.apps.bcpp_household.models import HouseholdStructure

from ..forms import HouseholdMemberForm
from ..models import HouseholdMember

from .base_household_member_admin import BaseHouseholdMemberAdmin


class HouseholdMemberInline(BaseTabularInline):
    model = HouseholdMember
    extra = 3


class HouseholdMemberAdmin(BaseHouseholdMemberAdmin):

    form = HouseholdMemberForm
    date_hierarchy = 'modified'
    actions = [export_as_csv_action(
        "Export as csv",
        fields=[
            'initials', 'gender', 'age_in_years', 'member_status', 'present_today', 'study_resident', 'relation',
            'eligible_member', 'eligible_subject'],
        extra_fields={'plot_identifier': 'household_structure__household__plot__plot_identifier'})]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
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
        return super(HouseholdMemberAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    fields = ['household_structure',
              'first_name',
              'initials',
              'gender',
              'age_in_years',
              'present_today',
              'inability_to_participate',
              'inability_to_participate_other',
              'study_resident',
              'relation',
              'personal_details_changed',
              'details_change_reason']

    radio_fields = {
        "gender": admin.VERTICAL,
        "relation": admin.VERTICAL,
        "present_today": admin.VERTICAL,
        "inability_to_participate": admin.VERTICAL,
        "study_resident": admin.VERTICAL,
    }

    list_display = ('first_name', 'initials',
                    'household_structure',
                    'updated',
                    'to_locator',
                    'hiv_history',
                    'relation',
                    'visit_attempts',
                    'member_status',
                    'inability_to_participate',
                    'eligible_member',
                    'eligible_subject',
                    'enrollment_checklist_completed',
                    'enrollment_loss_completed',
                    'reported',
                    'refused',
                    'is_consented',
                    'eligible_htc',
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

    list_filter = ('household_structure__survey__survey_name', 'present_today', 'study_resident',
                   'member_status', 'inability_to_participate', 'survival_status',
                   'eligible_member', 'eligible_subject', 'enrollment_checklist_completed',
                   'enrollment_loss_completed', 'reported',
                   'refused', 'is_consented', 'eligible_htc', 'target', 'hiv_history',
                   'household_structure__household__community',
                   'modified', 'hostname_created', 'user_created', 'visit_attempts',
                   'auto_filled',
                   'updated_after_auto_filled',
                   )

    def get_fields(self, request, obj=None):
        fields = self.all_required_fields()
        return [(None, {'fields': fields})]

    list_per_page = 15
admin.site.register(HouseholdMember, HouseholdMemberAdmin)
