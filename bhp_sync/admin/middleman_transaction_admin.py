from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_sync.models import MiddleManTransaction
from bhp_sync.actions import reset_outgoing_transaction_middle_as_consumed, reset_outgoing_transaction_middle_as_not_consumed, reset_outgoing_transaction_server_as_consumed, reset_outgoing_transaction_server_as_not_consumed


class MiddleManTransactionAdmin (BaseModelAdmin):

    list_display = ('tx_name', 'render', 'producer', 'is_consumed_middleman' ,'is_consumed_server' , 'is_error', 'consumer', 'consumed_datetime', 'action', 'tx_pk', 'timestamp', 'hostname_modified')

    list_filter = ('is_error', 'is_consumed_middleman', 'is_consumed_server', 'consumer', 'consumed_datetime', 'producer', 'action', 'tx_name', 'hostname_modified')

    search_fields = ('tx_pk', 'tx', 'timestamp', 'error')

    actions = [reset_outgoing_transaction_middle_as_consumed, reset_outgoing_transaction_middle_as_not_consumed, reset_outgoing_transaction_server_as_consumed, reset_outgoing_transaction_server_as_not_consumed]

admin.site.register(MiddleManTransaction, MiddleManTransactionAdmin)
