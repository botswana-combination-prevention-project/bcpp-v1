from django.contrib import admin
from bhp_data_manager.models import ActionItem
from bhp_registration.models import RegisteredSubject
from bhp_data_manager.forms import ActionItemForm
from base_admin import BaseAdmin


class ActionItemAdmin(BaseAdmin):

    form = ActionItemForm

    def __init__(self, *args, **kwargs):
        super(ActionItemAdmin, self).__init__(*args, **kwargs)
        self.search_fields.insert(0, 'registered_subject__pk')
        self.search_fields.insert(0, 'registered_subject__subject_identifier')
        self.list_display.insert(1, 'dashboard')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('registered_subject'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(pk=request.GET.get('registered_subject'))
        return super(ActionItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(ActionItem, ActionItemAdmin)
