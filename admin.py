from datetime import *
from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from autocomplete.views import autocomplete, AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin
from bhp_lab_receive.models import Receive
#from bhp_lab_receiveutils import AllocateReceiveIdentifier

class ReceiveAutocomplete(AutocompleteSettings):
    search_fields = ('^receive_identifier',)



class ReceiveAdmin(AutocompleteAdmin, MyModelAdmin):
    
    def save_model(self, request, obj, form, change):
        if not change:

            receive_identifier = None 
            #    AllocateReceiveIdentifier(
            #    request.user, 
            #    )

            obj.receive_identifier = receive_identifier['id']

        save = super(ReceiveAdmin, self).save_model(request, obj, form, change)

        return save

    def get_readonly_fields(self, request, obj = None):
        if obj: #In edit mode
            return ('receive_identifier',) + self.readonly_fields
        else:
            return self.readonly_fields     


    def change_view(self, request, object_id, extra_context=None):

        result = super(ReceiveAdmin, self).change_view(request, object_id, extra_context)        
        if request.GET.get('return_object')=='result': 
            try:
                oResult = Result.objects.get(pk=request.GET.get('object_id'))            
                result['Location'] = oResult.get_document_url()
            except:
                pass
        return result        
            
    list_display = ('patient', 'datetime_drawn', 'receive_datetime')        
    
    #inlines = [AliquotInlineAdmin]

admin.site.register(Receive, ReceiveAdmin)    
