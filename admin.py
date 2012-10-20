from datetime import datetime
from django.contrib import admin
from autocomplete.admin import AutocompleteAdmin
from bhp_common.models import MyModelAdmin
from lab_result.models import Result
from models import ResultItem


class ResultItemAdmin(AutocompleteAdmin, MyModelAdmin):

    def save_model(self, request, obj, form, change):

        obj.validation_datetime = datetime.today()
        obj.validation_username = request.user.username

        save = super(ResultItemAdmin, self).save_model(request, obj, form, change)
        return save

    def change_view(self, request, object_id, extra_context=None):

        result = super(ResultItemAdmin, self).change_view(request, object_id, extra_context)
        oResult = Result.objects.get(resultitem__pk=object_id)
        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
            result['Location'] = oResult.get_document_url()
        return result

    #override to disallow subject to be changed
    def get_readonly_fields(self, request, obj=None):
        if obj:  # In edit mode
            return ('result',) + self.readonly_fields
        else:
            return self.readonly_fields

    list_display = ('result', 'test_code', 'result_item_value', 'validation_status', 'result_item_datetime', 'result_item_operator', 'result_item_source_reference')
    search_fields = ['result__result_identifier', 'test_code__code', 'test_code__name', 'result_item_source_reference', ]
    list_filter = ('validation_status', 'test_code', 'result_item_datetime', 'modified')
    list_per_page = 15
admin.site.register(ResultItem, ResultItemAdmin)
