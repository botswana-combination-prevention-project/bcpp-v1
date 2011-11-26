
def reset_transaction(modeladmin, request, queryset):
    """ reset transaction by setting is_consumed = False"""
    for qs in queryset:
        qs.is_consumed = False
        qs.save()
            
reset_transaction.short_description = "Reset transactions by setting is_consumed to false"
