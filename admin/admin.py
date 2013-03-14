#from datetime import datetime
from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from bhp_sync.models import Transaction, RequestLog
from bhp_sync.actions import reset_transaction_as_not_consumed, reset_transaction_as_consumed


class TransactionAdmin (BaseModelAdmin):

    list_display = ('tx_name', 'producer', 'is_consumed', 'consumer', 'consumed_datetime', 'action', 'tx_pk', 'timestamp', 'hostname_modified')

    list_filter = ('is_consumed', 'consumer', 'consumed_datetime', 'producer', 'action', 'tx_name', 'hostname_modified')

    search_fields = ('tx_pk', 'tx', 'timestamp',)

    actions = [reset_transaction_as_not_consumed, reset_transaction_as_consumed, ]

admin.site.register(Transaction, TransactionAdmin)


class RequestLogAdmin(BaseModelAdmin):

    list_display = ('producer', 'request_datetime', 'status', 'comment')

admin.site.register(RequestLog, RequestLogAdmin)
