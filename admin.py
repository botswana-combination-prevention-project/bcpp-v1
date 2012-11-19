from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin, BaseStackedInline
from models import HBCDispatch, HBCDispatchItem


class HBCDispatchItemInline(BaseStackedInline):
    model = HBCDispatchItem


class HBCDispatchAdmin(BaseModelAdmin):
    #actions = [process_hbc_dispatch, ]
    ordering = ['-created', ]
    list_display = (
        'producer',
        'checkout_items',
        'created',
        'is_checked_out',
        'is_checked_in',
        'datetime_checked_out',
        'datetime_checked_in'
        )
    list_filter = (
        'producer',
        'created',
        'is_checked_out',
        'is_checked_in',
        'datetime_checked_out',
        'datetime_checked_in'
        )
    inlines = [HBCDispatchItemInline, ]
#admin.site.register(HBCDispatch, HBCDispatchAdmin)


class HBCDispatchItemAdmin(BaseModelAdmin):
    ordering = ['-created', 'item_identifier']
    list_display = (
        'hbc_dispatch',
        'producer',
        'item_identifier',
        'created',
        'is_checked_out',
        'is_checked_in',
        'datetime_checked_out',
        'datetime_checked_in'
        )
    list_filter = (
        'producer',
        'item_identifier',
        'created',
        'is_checked_out',
        'is_checked_in',
        'datetime_checked_out',
        'datetime_checked_in'
        )
#admin.site.register(HBCDispatchItem, HBCDispatchItemAdmin)