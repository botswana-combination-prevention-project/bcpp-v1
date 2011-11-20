from datetime import datetime
from django.contrib import admin
from bhp_common.models import MyModelAdmin
from models import Transaction, RequestLog, Producer


class TransactionAdmin (MyModelAdmin):

    list_display = ('tx_name', 'is_sent', 'producer', 'action', 'tx_pk', 'timestamp', 'hostname_modified')
    
    list_filter = ('is_sent', 'producer', 'action', 'tx_name','hostname_modified')
    
admin.site.register(Transaction, TransactionAdmin)

class Producer(MyModelAdmin):

    list_display = ('name', 'url', 'is_active')
    
admin.site.register(Producer, ProducerAdmin)

class RequestLog(MyModelAdmin):

    list_display = ('producer', 'request_datetime', 'status', 'comment')

admin.site.register(RequestLog, RequestLogAdmin)
