from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin, BaseStackedInline
from models import Dispatch, DispatchItem


class DispatchItemInline(BaseStackedInline):
    model = DispatchItem


class DispatchAdmin(BaseModelAdmin):
    ordering = ['-created', ]
    list_display = (
        'producer',
        'dispatch_items',
        'created',
        'is_dispatched',
        'dispatched_datetime',
        'returned_datetime'
        )
    list_filter = (
        'producer',
        'created',
        'is_dispatched',
        'dispatched_datetime',
        'returned_datetime'
        )
    inlines = [DispatchItemInline, ]
admin.site.register(Dispatch, DispatchAdmin)


class DispatchItemAdmin(BaseModelAdmin):
    ordering = ['-created', 'item_identifier']
    list_display = (
        'dispatch',
        'producer',
        'item_identifier',
        'created',
        'is_dispatched',
        'dispatched_datetime',
        'returned_datetime'
        )
    list_filter = (
        'producer',
        'item_identifier',
        'created',
        'is_dispatched',
        'dispatched_datetime',
        'returned_datetime'
        )
admin.site.register(DispatchItem, DispatchItemAdmin)