from django.contrib import admin

from ..models import NotebookPlotList

from ..forms import NotebookPlotListForm

from .base_household_model_admin import BaseHouseholdModelAdmin


class NotebookPlotListAdmin(BaseHouseholdModelAdmin):

    fields = ('plot_identifier',)
    list_display = ('plot_identifier',)

    form = NotebookPlotListForm

admin.site.register(NotebookPlotList, NotebookPlotListAdmin)
