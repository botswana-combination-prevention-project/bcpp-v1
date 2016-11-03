from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

# from ..actions import update_replaceables_action
from ..models import Replaceable


class ReplaceableAdmin(BaseModelAdmin):

    instructions = []

    fields = (
        'app_label',
        'model_name',
        'community',
        'plot_status',
        'item_identifier',
        'item_pk',
        'producer_name',
    )
    list_display = (
        'item_identifier', 'model_name', 'replaced', 'community', 'producer_name', 'plot_status', 'created')

    list_filter = ('replaced', 'community', 'plot_status', 'model_name', 'producer_name', 'replaced_reason')

    search_fields = ('item_pk', 'item_identifier', 'producer_name')

    # actions = [update_replaceables_action, ]

admin.site.register(Replaceable, ReplaceableAdmin)
