from django.contrib import admin

from ..forms import ReplacementHistoryForm
from ..models import ReplacementHistory

from .base_household_model_admin import BaseHouseholdModelAdmin


class ReplacementHistoryAdmin(BaseHouseholdModelAdmin):

    form = ReplacementHistoryForm
    fields = (
        'replacing_item',
        'replaced_item',
        'replacement_datetime',
        'replacement_reason'
    )
    list_display = ('replaced_item', 'replacing_item', 'replacement_datetime', 'replacement_reason')

    list_filter = ('replacement_datetime', 'replacement_reason')

    search_fields = ('replaced_item', 'replaced_item')

admin.site.register(ReplacementHistory, ReplacementHistoryAdmin)
