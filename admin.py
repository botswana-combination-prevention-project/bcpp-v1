#from datetime import datetime
from django.contrib import admin
from bhp_common.models import MyModelAdmin
from models import Transaction, IncomingTransaction, OutgoingTransaction, RequestLog, Producer
from actions import reset_transaction_as_not_consumed, reset_transaction_as_consumed, reset_producer_status, \
                    reset_incomingtransaction_error_status


class TransactionAdmin (MyModelAdmin):

    list_display = ('tx_name', 'producer', 'is_consumed', 'consumer', 'consumed_datetime', 'action', 'tx_pk', 'timestamp', 'hostname_modified')
    
    list_filter = ('is_consumed', 'consumer', 'consumed_datetime', 'producer', 'action', 'tx_name','hostname_modified')
    
    search_fields = ('tx_pk', 'tx', 'timestamp',)
    
    actions = [reset_transaction_as_not_consumed, reset_transaction_as_consumed,]
    
admin.site.register(Transaction, TransactionAdmin)


class IncomingTransactionAdmin (MyModelAdmin):

    list_display = ('tx_name', 'producer', 'is_consumed', 'is_error', 'consumer', 'consumed_datetime', 'action', 'tx_pk', 'timestamp', 'hostname_modified')
    
    list_filter = ('is_consumed', 'is_error', 'consumer', 'consumed_datetime', 'producer', 'action', 'tx_name','hostname_modified')
    
    search_fields = ('tx_pk', 'tx', 'timestamp','error')
    
    actions = [reset_transaction_as_not_consumed, reset_transaction_as_consumed, reset_incomingtransaction_error_status,]
    
admin.site.register(IncomingTransaction, IncomingTransactionAdmin)


class OutgoingTransactionAdmin (MyModelAdmin):

    list_display = ('tx_name', 'producer', 'is_consumed', 'is_error', 'consumer', 'consumed_datetime', 'action', 'tx_pk', 'timestamp', 'hostname_modified')
    
    list_filter = ('is_consumed', 'is_error', 'consumer', 'consumed_datetime', 'producer', 'action', 'tx_name','hostname_modified')
    
    search_fields = ('tx_pk', 'tx', 'timestamp', 'error')
    
    actions = [reset_transaction_as_not_consumed, reset_transaction_as_consumed,]
    
admin.site.register(OutgoingTransaction, OutgoingTransactionAdmin)

class ProducerAdmin(MyModelAdmin):

    list_display = ('name', 'url', 'is_active', 'sync_datetime', 'sync_status', 'comment')
    list_filter = ('is_active', 'sync_datetime', 'sync_status',)
    
    actions = [reset_producer_status,]
    
admin.site.register(Producer, ProducerAdmin)

class RequestLogAdmin(MyModelAdmin):

    list_display = ('producer', 'request_datetime', 'status', 'comment')

admin.site.register(RequestLog, RequestLogAdmin)


