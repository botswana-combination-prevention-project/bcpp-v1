from bhp_lab_tracker.classes import lab_tracker


def update_lab_tracker(modeladmin, request, queryset):
    if not lab_tracker.all():
        modeladmin.message_user(request, 'Lab tracker is empty. Nothing to do.')
    else:
        num_updated = lab_tracker.update_all(False)
        modeladmin.message_user(request, 'Updated {0} items for the lab tracker history model.'.format(num_updated))

update_lab_tracker.short_description = "Update lab tracker history model"
