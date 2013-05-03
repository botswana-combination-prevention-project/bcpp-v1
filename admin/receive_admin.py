from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from autocomplete.views import AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin
from lab_receive.models import Receive


class ReceiveAutocomplete(AutocompleteSettings):
    search_fields = ('^receive_identifier',)


class ReceiveAdmin(AutocompleteAdmin, BaseModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:  # In edit mode
            return ('receive_identifier',) + self.readonly_fields
        else:
            return self.readonly_fields

#    def change_view(self, request, object_id, extra_context=None):
#
#        result = super(ReceiveAdmin, self).change_view(request, object_id, extra_context)
#        if request.GET.get('return_object') == 'result':
#            try:
#                result = Result.objects.get(pk=request.GET.get('object_id'))
#                result['Location'] = result.get_document_url()
#            except:
#                pass
#        return result

    list_display = ('receive_identifier', 'patient', 'drawn_datetime', 'receive_datetime', 'protocol')
    search_fields = ('receive_identifier', 'patient__subject_identifier', 'protocol')
    list_filter = ('drawn_datetime', 'receive_datetime', 'protocol')
    list_per_page = 15

admin.site.register(Receive, ReceiveAdmin)
