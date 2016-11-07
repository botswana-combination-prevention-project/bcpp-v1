from django.contrib import admin

from edc_base.modeladmin.mixins import TabularInlineMixin
from edc_export.actions import export_as_csv_action

from ..admin_site import bcpp_household_member_admin
from ..forms import HouseholdMemberForm
from ..models import HouseholdMember

from .modeladmin_mixins import HouseholdMemberAdminMixin


class HouseholdMemberInline(TabularInlineMixin, admin.TabularInline):
    model = HouseholdMember
    extra = 3


@admin.register(HouseholdMember, site=bcpp_household_member_admin)
class HouseholdMemberAdmin(HouseholdMemberAdminMixin, admin.ModelAdmin):

    form = HouseholdMemberForm
    date_hierarchy = 'modified'
    actions = [export_as_csv_action(
        "Export as csv",
        fields=[
            'initials', 'gender', 'age_in_years', 'member_status', 'present_today', 'study_resident', 'relation',
            'eligible_member', 'eligible_subject'],
        extra_fields={'plot_identifier': 'household_structure__household__plot__plot_identifier'})]

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
        "personal_details_changed": admin.VERTICAL,
        "details_change_reason": admin.VERTICAL
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

    def get_fieldsets(self, request, obj=None):
        fields = self.fields
        if not obj:
            try:
                fields.remove('personal_details_changed')
                fields.remove('details_change_reason')
            except ValueError:
                pass
        return [(None, {'fields': fields})]

    list_per_page = 15
