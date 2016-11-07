from bcpp_household.models import HouseholdStructure

from ..models import HouseholdMember


class HouseholdMemberAdminMixin:

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
        if db_field.name == "household_member":
            if request.GET.get('household_member'):
                kwargs["queryset"] = HouseholdMember.objects.filter(
                    id__exact=request.GET.get('household_member', 0))
            else:
                self.readonly_fields = list(self.readonly_fields)
                try:
                    self.readonly_fields.index('household_member')
                except ValueError:
                    self.readonly_fields.append('household_member')
        return super(HouseholdMemberAdminMixin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('household_member', 'household_structure', ) + self.readonly_fields
        else:
            return self.readonly_fields
