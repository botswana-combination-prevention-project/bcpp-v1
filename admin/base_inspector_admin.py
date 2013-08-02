from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_inspector.models import BaseInspector

class BaseInspectorAdmin(BaseModelAdmin):
    
    list_display = ['item_identifier', 'app_name', 'model_name', 'is_consumed']

    list_filter = ['item_identifier', 'app_name', 'model_name', 'is_consumed']

    search_fields = ['item_identifier', 'app_name', 'model_name', 'is_consumed']

    #actions = [reset_transaction_as_not_consumed, reset_transaction_as_consumed, reset_incomingtransaction_error_status, set_incomingtransaction_as_ignore_status, reset_incomingtransaction_ignore_status ]
#admin.site.register(BaseInspector, BaseInspectorAdmin)