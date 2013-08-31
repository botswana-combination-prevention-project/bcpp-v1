from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_lab_tracker.models import HistoryModel, HistoryModelError, DefaultValueLog
from bhp_lab_tracker.actions import update_lab_tracker


class HistoryModelAdmin(BaseModelAdmin):
    list_display = ('subject_identifier', 'dashboard', 'subject_type', 'group_name', 'test_code', 'value', 'value_datetime', 'source_model_name', 'source_app_label', 'source_identifier', 'history_datetime', 'modified')
    search_fields = ('subject_identifier', 'value', 'source_identifier')
    list_filter = ('subject_type', 'group_name', 'source_model_name', 'source_app_label', 'test_code', 'modified')
    actions = [update_lab_tracker, ]
    date_hierarchy = 'value_datetime'
admin.site.register(HistoryModel, HistoryModelAdmin)


class HistoryModelErrorAdmin(BaseModelAdmin):
    list_display = ('subject_identifier', 'group_name', 'test_code', 'value', 'value_datetime', 'source_model_name', 'source_app_label', 'source_identifier', 'history_datetime', 'modified')
    search_fields = ('subject_identifier', 'value', 'error_message')
    list_filter = ('group_name', 'source_model_name', 'source_app_label', 'test_code', 'modified')
    date_hierarchy = 'value_datetime'
admin.site.register(HistoryModelError, HistoryModelErrorAdmin)


class DefaultValueLogAdmin(BaseModelAdmin):
    list_display = ('subject_identifier', 'group_name', 'value', 'value_datetime', 'modified')
    search_fields = ('subject_identifier', 'error_message')
    list_filter = ('group_name', 'subject_type', 'modified')
    date_hierarchy = 'value_datetime'
admin.site.register(DefaultValueLog, DefaultValueLogAdmin)
