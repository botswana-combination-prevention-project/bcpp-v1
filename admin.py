from datetime import datetime
from django.contrib import admin
from bhp_common.models import MyModelAdmin
from models import Transaction, RequestLog, Producer
from actions import reset_transaction


class TransactionAdmin (MyModelAdmin):

    list_display = ('tx_name', 'producer', 'is_consumed', 'consumer', 'consumed_datetime', 'action', 'tx_pk', 'timestamp', 'hostname_modified')
    
    list_filter = ('is_consumed', 'consumer', 'consumed_datetime', 'producer', 'action', 'tx_name','hostname_modified')
    
    search_fields = ('tx_pk', 'tx')
    
    actions = [reset_transaction, ]
    
admin.site.register(Transaction, TransactionAdmin)

class ProducerAdmin(MyModelAdmin):

    list_display = ('name', 'url', 'is_active')
    
admin.site.register(Producer, ProducerAdmin)

class RequestLogAdmin(MyModelAdmin):

    list_display = ('producer', 'request_datetime', 'status', 'comment')

admin.site.register(RequestLog, RequestLogAdmin)
