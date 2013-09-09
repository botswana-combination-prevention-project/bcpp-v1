from lab_clinic_api.models import Receive


def clear_stale_error_messages(modeladmin, request, queryset):

    for qs in queryset:
        n = 0
        # check if receive identifier is found in receive
        if qs.model_name == 'Receive':
            if Receive.objects.filter(receive_identifier=qs.identifier).exists():
                qs.delete()
                n += 1
    modeladmin.message_user(request, 'Removed {0} error messages'.format(n))
clear_stale_error_messages.short_description = "Clear stale error messages"
