from django.contrib import admin

from ..actions import update_increaseplotradius_action
from ..filters import ActionFilter
from ..forms import IncreasePlotRadiusForm
from ..models import IncreasePlotRadius

from .base_household_model_admin import BaseHouseholdModelAdmin


class IncreasePlotRadiusAdmin(BaseHouseholdModelAdmin):

    form = IncreasePlotRadiusForm

    fields = ('radius', )
    list_display = ('plot', 'radius', 'action', 'status', 'producer', 'modified', 'created')
    list_filter = (ActionFilter, )
    search_fields = ('plot__plot_identifier', 'plot__hostname_modified')
    actions = [update_increaseplotradius_action]

admin.site.register(IncreasePlotRadius, IncreasePlotRadiusAdmin)
