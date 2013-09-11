from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from lab_receive.models import Receive


class ReceiveAdmin(AutocompleteAdmin, BaseModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:  # In edit mode
            return ('receive_identifier',) + self.readonly_fields
        else:
            return self.readonly_fields

    list_display = ('receive_identifier', 'patient', 'drawn_datetime', 'receive_datetime', 'protocol')
    search_fields = ('receive_identifier', 'patient__subject_identifier', 'protocol')
    list_filter = ('drawn_datetime', 'receive_datetime', 'protocol')
    list_per_page = 15
    date_hierarchy = 'drawn_datetime'
admin.site.register(Receive, ReceiveAdmin)
