from datetime import *
from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from autocomplete.views import autocomplete, AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin
from lab_aliquot.models import Aliquot, AliquotCondition, AliquotType


class ReceiveAutocomplete(AutocompleteSettings):

    search_fields = ('^receive_identifier',)




class AliquotTypeAutocomplete(AutocompleteSettings):

    search_fields = ('^numeric_code', '^alpha_code','^name', )


autocomplete.register(Aliquot.receive, ReceiveAutocomplete)

autocomplete.register(Aliquot.aliquot_type, AliquotTypeAutocomplete)


class AliquotTypeAdmin(MyModelAdmin):

    list_display = ('alpha_code', 'numeric_code', 'name', 'created', 'modified')
    
    ordering = ['name']
    
admin.site.register(AliquotType,AliquotTypeAdmin)


class AliquotConditionAdmin(MyModelAdmin):

    list_display = ('display_index', 'name', 'short_name', 'field_name', 'created', 'modified')

    ordering = ['display_index']

admin.site.register(AliquotCondition,AliquotConditionAdmin)


class AliquotAdmin(AutocompleteAdmin, MyModelAdmin):
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.aliquot_identifier = self.model.objects.get_identifier(
                parent_identifier = request.POST.get('parent_identifier'),
                aliquot_type = request.POST.get('aliquot_type'),
                ) 
            
        save = super(AliquotAdmin, self).save_model(request, obj, form, change)
        return save

    def get_readonly_fields(self, request, obj = None):
        if obj: #In edit mode
            return ('aliquot_type','receive','original_measure',) + self.readonly_fields
        else:
            return self.readonly_fields     

    fields = ('aliquot_identifier', 'receive', 'aliquot_type', 'medium', 'original_measure', 'current_measure',  'measure_units', 'condition', 'status', 'comment')        

    list_display = ('aliquot_identifier', 'aliquot_type', 'original_measure', 'current_measure', 'measure_units', 'condition', 'receive')        

    readonly_fields = ('aliquot_identifier',)        

admin.site.register(Aliquot, AliquotAdmin)    



