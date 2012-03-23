from bhp_sync.classes import SerializeToTransaction

def serialize(modeladmin, request, queryset):
    
    """ for a model instance serializing to outgoing"""
    serialize_to_transaction = SerializeToTransaction()
                
    for instance in queryset:
        
        serialize_to_transaction.serialize(instance.__class__, instance)

serialize.short_description = "Send as Outgoing Transaction"


def reset_transaction_as_not_consumed(modeladmin, request, queryset):
    """ reset transaction by setting is_consumed = False"""
    for qs in queryset:
        qs.is_consumed = False
        qs.consumer = None
        qs.save()
            
reset_transaction_as_not_consumed.short_description = "Set transactions as NOT consumed (is_consumed=False)"

def reset_transaction_as_consumed(modeladmin, request, queryset):
    """ reset transaction by setting is_consumed = True"""
    for qs in queryset:
        qs.is_consumed = True
        qs.save()
            
reset_transaction_as_consumed.short_description = "Set transactions as consumed (is_consumed=True)"

def reset_producer_status(modeladmin, request, queryset):
    """ reset producer status to '-' """
    for qs in queryset:
        if qs.is_active:
            qs.sync_status = '-'
            qs.save()
            
reset_producer_status.short_description = "Reset producer status to '-'"

def reset_incomingtransaction_error_status(modeladmin, request, queryset):
    """ reset producer status to '-' """
    for qs in queryset:
        qs.is_error = False
        qs.error = None
        qs.save()
            
reset_incomingtransaction_error_status.short_description = "Reset transaction error status (is_error=False)"

"""
def set_incomingtransaction_postpone_status(modeladmin, request, queryset):
    "" reset producer status to '-' ""
    for qs in queryset:
        qs.is_postpone = True
        qs.save()
            
set_incomingtransaction_postpone_status.short_description = "Set transaction status to postpone (is_postpone = True)"
"""