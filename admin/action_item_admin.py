from django.contrib import admin
from django.contrib.auth.models import Group
from bhp_data_manager.models import ActionItem
from bhp_registration.models import RegisteredSubject
from bhp_data_manager.forms import ActionItemForm
from base_admin import BaseAdmin
from bhp_data_manager.classes import data_manager


class ActionItemAdmin(BaseAdmin):

    form = ActionItemForm

    def __init__(self, *args, **kwargs):
        super(ActionItemAdmin, self).__init__(*args, **kwargs)
        self.search_fields.insert(0, 'registered_subject__pk')
        self.search_fields.insert(0, 'registered_subject__subject_identifier')
        self.list_display.insert(1, 'dashboard')
        # save_model expects bhp_data_manager specific user groups

    def save_model(self, request, obj, form, change):
        # check for bhp_data_manager user groups
        data_manager.check_groups()
        user = request.user
        if not user.is_superuser:
            user_groups = [group.name for group in Group.objects.filter(user__username=request.user)]
            if not user_groups:
                obj.action_group = 'no group'
            elif obj.action_group not in user_groups:
                obj.action_group = user_groups[0]
            else:
                pass
            if obj.status == 'closed' and ('data_manager' not in user_groups and 'action_manager' not in user_groups):
                obj.status = 'open'
        super(ActionItemAdmin, self).save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('registered_subject'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(pk=request.GET.get('registered_subject'))
        return super(ActionItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(ActionItem, ActionItemAdmin)
