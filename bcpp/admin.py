from django.contrib import admin

from bcpp_household.admin_site import bcpp_household_admin
from .models import AvailablePlot


@admin.register(AvailablePlot, site=bcpp_household_admin)
class NotebookPlotListAdmin(admin.ModelAdmin):

    fields = ('plot_identifier',)
    list_display = ('plot_identifier',)

    form = AvailablePlot
