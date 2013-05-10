from datetime import datetime
from django.contrib import admin
from autocomplete.admin import AutocompleteAdmin
from bhp_base_admin.admin import BaseModelAdmin
from lab_result_item.models import ResultItem


class ResultItemAdmin(AutocompleteAdmin, BaseModelAdmin):

    def save_model(self, request, obj, form, change):

        obj.validation_datetime = datetime.today()
        obj.validation_username = request.user.username

        save = super(ResultItemAdmin, self).save_model(request, obj, form, change)
        return save

    def get_readonly_fields(self, request, obj=None):
        if obj:  # In edit mode
            return ('result',) + self.readonly_fields
        else:
            return self.readonly_fields

    list_display = ('result', 'test_code', 'result_item_value', 'validation_status', 'result_item_datetime', 'result_item_operator', 'result_item_source_reference')
    search_fields = ['result__result_identifier', 'test_code__code', 'test_code__name', 'result_item_source_reference', 'result__order__aliquot__receive__receive_identifier']
    list_filter = ('validation_status', 'test_code', 'result_item_datetime', 'modified')
    list_per_page = 15
admin.site.register(ResultItem, ResultItemAdmin)
