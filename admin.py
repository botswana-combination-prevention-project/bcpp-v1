from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin, BaseStackedInline
from models import DispatchContainerRegister, DispatchItemRegister
from bhp_dispatch.actions import set_is_dispatched


class DispatchItemRegisterInline(BaseStackedInline):
    model = DispatchItemRegister
    extra = 0


class DispatchContainerRegisterAdmin(BaseModelAdmin):
    date_hierarchy = 'dispatch_datetime'
    ordering = ['-created', ]
    list_display = (
        'producer',
        'to_items',
        'container_model_name',
        'container_identifier',
        'created',
        'is_dispatched',
        'dispatch_datetime',
        'return_datetime'
        )
    list_filter = (
        'producer',
        'container_identifier',
        'created',
        'is_dispatched',
        'dispatch_datetime',
        'return_datetime'
        )
    search_fields = ('id', 'container_identifier', )
    inlines = [DispatchItemRegisterInline, ]
admin.site.register(DispatchContainerRegister, DispatchContainerRegisterAdmin)


class DispatchItemRegisterAdmin(BaseModelAdmin):
    date_hierarchy = 'dispatch_datetime'
    ordering = ['-created', 'item_identifier']
    list_display = (
        'producer',
        'item_model_name',
        'created',
        'is_dispatched',
        'dispatch_datetime',
        'return_datetime'
        )
    list_filter = (
        'dispatch_container_register',
        'producer',
        'item_model_name',
        'created',
        'is_dispatched',
        'dispatch_datetime',
        'return_datetime'
        )
    search_fields = ('dispatch_container_register__container_identifier', 'item_identifier')
    actions = [set_is_dispatched, ]

admin.site.register(DispatchItemRegister, DispatchItemRegisterAdmin)