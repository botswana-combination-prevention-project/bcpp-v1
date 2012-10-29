from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from models import HistoryModel, HistoryModelError, DefaultValueLog


class HistoryModelAdmin(BaseModelAdmin):
    list_display = ('subject_identifier', 'group_name', 'test_code', 'value', 'value_datetime', 'source_identifier', 'history_datetime', 'modified')
    search_fields = ('subject_identifier', 'value')
    list_filter = ('group_name', 'source', 'test_code', 'modified')
admin.site.register(HistoryModel, HistoryModelAdmin)


class HistoryModelErrorAdmin(BaseModelAdmin):
    list_display = ('subject_identifier', 'group_name', 'test_code', 'value', 'value_datetime', 'source_identifier', 'history_datetime', 'modified')
    search_fields = ('subject_identifier', 'value', 'error_message')
    list_filter = ('group_name', 'source', 'test_code', 'modified')
admin.site.register(HistoryModelError, HistoryModelErrorAdmin)


class DefaultValueLogAdmin(BaseModelAdmin):
    list_display = ('subject_identifier', 'group_name', 'value_datetime', 'modified')
    search_fields = ('subject_identifier', 'error_message')
    list_filer = ('group_name', 'modified')
admin.site.register(DefaultValueLog, DefaultValueLogAdmin)
