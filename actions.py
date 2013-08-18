from bhp_lab_tracker.classes import site_lab_tracker


def update_lab_tracker(modeladmin, request, queryset):
    if not site_lab_tracker.all():
        modeladmin.message_user(request, 'Lab tracker registry is empty. Nothing to do.')
    else:
        num_updated = site_lab_tracker.update_all(False)
        modeladmin.message_user(request, 'Updated {0} items for the lab tracker history model.'.format(num_updated))

update_lab_tracker.short_description = "Update lab tracker history model"
