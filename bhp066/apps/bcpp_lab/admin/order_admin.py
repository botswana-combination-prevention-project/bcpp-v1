from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin, BaseTabularInline

from ..models import Order, OrderItem


class OrderItemInlineAdmin(BaseTabularInline):
    model = OrderItem
    fields = ('aliquot', 'panel', 'order_datetime', 'order_identifier', 'subject_identifier')
    readonly_fields = ('aliquot', 'order_identifier', 'subject_identifier')


class OrderItemAdmin(BaseModelAdmin):

    list_display = ('order_identifier', 'aliquot', 'panel', 'order_datetime', 'subject_identifier')

admin.site.register(OrderItem, OrderItemAdmin)


class OrderAdmin(BaseModelAdmin):

    list_display = ('pk', 'order_datetime')
    list_filter = ("order_datetime", )
    inlines = [OrderItemInlineAdmin, ]

admin.site.register(Order, OrderAdmin)
