from datetime import datetime

from .models import Order, OrderItem


def create_order(modeladmin, request, queryset):
    order_datetime = datetime.today()
    order = Order.objects.create(order_datetime=order_datetime)
    for aliquot in queryset:
        OrderItem.objects.create(order=order, aliquot=aliquot, order_datetime=order_datetime)
create_order.short_description = "Create order from selected aliquots"
