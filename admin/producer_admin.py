from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_sync.models import Producer
from bhp_sync.actions import reset_producer_status


class ProducerAdmin(BaseModelAdmin):

    list_display = ('name', 'url', 'is_active', 'sync_datetime', 'sync_status', 'comment')
    list_filter = ('is_active', 'sync_datetime', 'sync_status',)

    actions = [reset_producer_status]

admin.site.register(Producer, ProducerAdmin)
