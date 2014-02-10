from django.contrib import admin
from edc.base.admin.admin import BaseTabularInline, BaseModelAdmin
from edc.export.actions import export_as_csv_action
from apps.bcpp_household.models import HouseholdStructure
from ..models import HouseholdMember
from ..forms import HouseholdMemberForm


class AbsenteeVisitAtempts(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Current Absentee visit attempts'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'visit_attempts'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        values = ['0', '1', '2', '3']
        visit_attempts_tuples = []
        visit_attempts_tuples.append((values[0], values[0]))
        visit_attempts_tuples.append((values[1], values[1]))
        visit_attempts_tuples.append((values[2], values[2]))
        visit_attempts_tuples.append((values[3], values[3]))
        return visit_attempts_tuples

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(member_status='ABSENT', visit_attempts=self.value())
        else:
            return queryset

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
                    'visit_attempts',
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
                    'modified', 'hostname_created', AbsenteeVisitAtempts)

    #readonly_fields = ('absentee_visit_attempts', )
    list_per_page = 25
admin.site.register(HouseholdMember, HouseholdMemberAdmin)
