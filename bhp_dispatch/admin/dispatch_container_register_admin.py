from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin, BaseStackedInline
from bhp_dispatch.models import DispatchContainerRegister, DispatchItemRegister


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
