from django.contrib import admin

from edc.base.admin.admin import BaseModelAdmin

from ..forms import HouseholdEnumerationRefusalForm
from ..models import HouseholdEnumerationRefusal, Household


class HouseholdEnumerationRefusalAdmin(BaseModelAdmin):

    form = HouseholdEnumerationRefusalForm
    date_hierarchy = 'modified'
    list_per_page = 30

    fields = (
        'household',
        'report_datetime',
        'reason',
        'reason_other',
        'comment')

    radio_fields = {
        'reason': admin.VERTICAL,
        }

    list_display = ('household', 'report_datetime', 'created')

    list_filter = ('report_datetime', 'created',)

    search_fields = ('household__household_identifier', 'community', 'id', 'plot__id')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household":
            kwargs["queryset"] = Household.objects.filter(id__exact=request.GET.get('household', 0))
        return super(HouseholdEnumerationRefusalAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(HouseholdEnumerationRefusal, HouseholdEnumerationRefusalAdmin)
