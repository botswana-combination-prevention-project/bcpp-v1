
def reset_transaction_as_not_consumed(modeladmin, request, queryset):
    """ reset transaction by setting is_consumed = False"""
    for qs in queryset:
        qs.is_consumed = False
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

