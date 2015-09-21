from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import HouseholdRefusalForm
from ..models import HouseholdRefusal, HouseholdStructure


class HouseholdRefusalAdmin(BaseModelAdmin):

    form = HouseholdRefusalForm
    date_hierarchy = 'modified'
    list_per_page = 30

    fields = (
        'household_structure',
        'report_datetime',
        'reason',
        'reason_other',
        'comment')

    radio_fields = {'reason': admin.VERTICAL}

    list_display = ('household_structure', 'report_datetime', 'created')

    list_filter = ('report_datetime', 'created', 'household_structure__household__community')

    search_fields = ('household_structure__household__household_identifier', 'community', 'id', 'plot__id')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_structure":
            kwargs["queryset"] = HouseholdStructure.objects.filter(id__exact=request.GET.get('household_structure', 0))
        return super(HouseholdRefusalAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(HouseholdRefusal, HouseholdRefusalAdmin)
