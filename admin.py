from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin, BaseStackedInline
from models import Dispatch, DispatchItem
from bhp_dispatch.actions import set_is_dispatched


class DispatchItemInline(BaseStackedInline):
    model = DispatchItem
    extra = 0


class DispatchAdmin(BaseModelAdmin):
    date_hierarchy = 'dispatch_datetime'
    ordering = ['-created', ]
    list_display = (
        'producer',
        'to_items',
        'created',
        'is_dispatched',
        'dispatch_datetime',
        'return_datetime'
        )
    list_filter = (
        'producer',
        'created',
        'is_dispatched',
        'dispatch_datetime',
        'return_datetime'
        )
    search_fields = ('id', )
    inlines = [DispatchItemInline, ]
admin.site.register(Dispatch, DispatchAdmin)


class DispatchItemAdmin(BaseModelAdmin):
    date_hierarchy = 'dispatch_datetime'
    ordering = ['-created', 'item_identifier']
    list_display = (
        'dispatch',
        'producer',
        'item_identifier',
        'created',
        'is_dispatched',
        'dispatch_datetime',
        'return_datetime'
        )
    list_filter = (
        'producer',
        'item_identifier',
        'created',
        'is_dispatched',
        'dispatch_datetime',
        'return_datetime'
        )
    search_fields = ('dispatch__pk', 'item_identifier', 'subject_identifiers')
    actions = [set_is_dispatched, ]

admin.site.register(DispatchItem, DispatchItemAdmin)