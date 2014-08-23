from django.contrib import admin

from apps.bcpp_household.admin.base_household_model_admin import BaseHouseholdModelAdmin
from ..models import Plot

from ..models import IncreasePlotRadius
from ..forms import IncreasePlotRadiusForm


class IncreasePlotRadiusAdmin(BaseHouseholdModelAdmin):

    form = IncreasePlotRadiusForm

    fields = (
        'plot',
        'radius'
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "plot":
            kwargs["queryset"] = Plot.objects.filter(id__exact=request.GET.get('plot', 0))
        return super(IncreasePlotRadiusAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(IncreasePlotRadius, IncreasePlotRadiusAdmin)
