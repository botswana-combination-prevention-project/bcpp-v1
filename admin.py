from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from models import HistoryModel


class HistoryModelAdmin(BaseModelAdmin):
    list_display = ('subject_identifier', 'group_name', 'test_code', 'value', 'value_datetime')
    search_fields = ('subject_identifier', 'value')
    list_filter = ('group_name', 'test_code')
admin.site.register(HistoryModel, HistoryModelAdmin)
