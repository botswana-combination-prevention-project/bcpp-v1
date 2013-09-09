from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin, BaseStackedInline
from bhp_dispatch.models import DispatchItemRegister
from bhp_dispatch.actions import set_is_dispatched


class DispatchItemRegisterInline(BaseStackedInline):
    model = DispatchItemRegister
    extra = 0


class DispatchItemRegisterAdmin(BaseModelAdmin):
    date_hierarchy = 'dispatch_datetime'
    ordering = ['-created', 'item_identifier']
    list_display = (
        'dispatch_container_register',
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
