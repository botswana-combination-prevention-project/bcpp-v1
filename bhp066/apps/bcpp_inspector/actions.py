

def set_inspectors_as_confirmed(modeladmin, request, queryset):
    """ set inspectors as confirmed"""
    for qs in queryset:
        qs.is_confirmed = True
        qs.save()
set_inspectors_as_confirmed.short_description = "Set Inspector Models as confirmed (is_confirmed=True)"
