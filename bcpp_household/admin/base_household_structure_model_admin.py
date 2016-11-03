from edc.export.actions import export_as_csv_action
from edc_base.modeladmin.admin import BaseModelAdmin

from ..models import HouseholdStructure


class BaseHouseholdStructureModelAdmin(BaseModelAdmin):

    actions = [export_as_csv_action(
        "Export as csv", fields=[], exclude=['id', ]
    )]

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
        return super(BaseHouseholdStructureModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
