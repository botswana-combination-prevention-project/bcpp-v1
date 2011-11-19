from datetime import datetime
from django.contrib import admin
from bhp_common.models import MyModelAdmin
from models import Transaction


class TransactionAdmin (MyModelAdmin):

    list_display = ('tx_name', 'is_sent', 'producer', 'action', 'tx_pk', 'timestamp', 'hostname_modified')
    
    list_filter = ('is_sent', 'producer', 'action', 'tx_name','hostname_modified')
    
admin.site.register(Transaction, TransactionAdmin)


