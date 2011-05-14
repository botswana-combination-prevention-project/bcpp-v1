from datetime import *
from django.contrib import admin
from autocomplete.views import autocomplete, AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin

from bhp_common.models import MyModelAdmin, MyStackedInline, MyTabularInline
from models import Panel, Aliquot, AliquotType, AliquotCondition
from models import Receive, Result, Order, ResultItem, AliquotMedium, TidPanelMapping, PanelGroup, ResultSource
from utils import AllocateAliquotIdentifier, AllocateReceiveIdentifier


class PatientAutocomplete(AutocompleteSettings):
    search_fields = ('^subject_identifier',)
autocomplete.register(Receive.patient, PatientAutocomplete)

class AliquotAutocomplete(AutocompleteSettings):
    search_fields = ('^aliquot_identifier',)
autocomplete.register(Order.aliquot, AliquotAutocomplete)

class OrderAutocomplete(AutocompleteSettings):
    search_fields = ('^order_identifier',)
autocomplete.register(Result.order, OrderAutocomplete)

class ResultAutocomplete(AutocompleteSettings):
    search_fields = ('^result_identifier',)
autocomplete.register(ResultItem.result, ResultAutocomplete)

class PanelAdmin(MyModelAdmin):
    list_display = ('name','panel_group')
    search_fields = ['name']
admin.site.register(Panel, PanelAdmin)

class PanelGroupAdmin(MyModelAdmin):
    list_display = ('name',)
admin.site.register(PanelGroup, PanelGroupAdmin)

class TidPanelMappingAdmin(MyModelAdmin):
    list_display = ('tid','panel')
admin.site.register(TidPanelMapping, TidPanelMappingAdmin)

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
    def get_readonly_fields(self, request, obj = None):
        if obj: #In edit mode
            return ('result',) + self.readonly_fields
        else:
            return self.readonly_fields  
     
    #readonly_fields = ( 'result', )    
    list_display = ( 'result', 'test_code', 'result_item_value', 'validation_status', 'result_item_datetime', 'result_item_operator', 'result_item_source_reference' )
    search_fields=['result__result_identifier', 'test_code__code','test_code__name', 'result_item_source_reference',]    
        
admin.site.register(ResultItem, ResultItemAdmin)


class ResultItemInlineAdmin(MyTabularInline):
    extra=0
    model = ResultItem

class ResultSourceAdmin(MyModelAdmin):
    pass
admin.site.register(ResultSource, ResultSourceAdmin)    

class ResultAdmin(AutocompleteAdmin, MyModelAdmin):

    def save_model(self, request, obj, form, change):
        if not change:
            obj.result_identifier = AllocateResultIdentifier(
                request.user, 
                request.POST.get('order'),
                )
        save = super(ResultAdmin, self).save_model(request, obj, form, change)
        return save
      
    def change_view(self, request, object_id, extra_context=None):

        response = super(ResultAdmin, self).change_view(request, object_id, extra_context)

        oResult = Result.objects.get(id__exact=object_id)
        
        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
            response['Location'] = oResult.get_document_url()
        return response
    

    #override to disallow subject to be changed
    def get_readonly_fields(self, request, obj = None):
        if obj: #In edit mode
            return ('order',) + self.readonly_fields
        else:
            return self.readonly_fields  
    
    #override, limit dropdown in add_view to id passed in the URL        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "order":
            kwargs["queryset"] = Order.objects.filter(id__exact=request.GET.get('order', 0))
        return super(ResultAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)   

    list_display = ('result_identifier', 'result_datetime',  'release_status', 'order', )
    search_fields = ('result_identifier', 'release_status')    
    filter_fields - ('result_datetime')

    #fields = ('order', 'result_datetime', 'release_status', 'release_datetime', 'comment')
    #inlines = [ResultItemInlineAdmin]
    
admin.site.register(Result, ResultAdmin)


class OrderAdmin(AutocompleteAdmin,MyModelAdmin):

    def save_model(self, request, obj, form, change):
    
        if change:
            obj.user_modified=request.user
    
        save = super(OrderAdmin, self).save_model(request, obj, form, change)
        return save


    #override to disallow subject to be changed
    def get_readonly_fields(self, request, obj = None):
        if obj: #In edit mode
            return ('aliquot','order_identifier',) + self.readonly_fields
        else:
            return self.readonly_fields  
    
    #override, limit dropdown in add_view to id passed in the URL        
    #def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #    if db_field.name == "aliquot":
    #        kwargs["queryset"] = Aliquot.objects.filter(id__exact=request.GET.get('aliquot', 0))
    #    return super(OrderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)   

    fields = ('order_identifier', 'order_datetime', 'panel', 'aliquot', 'comment', 'dmis_reference', )
    list_display = ('order_identifier', 'order_datetime', 'panel', 'aliquot', 'dmis_reference')
admin.site.register(Order, OrderAdmin)

class AliquotMediumAdmin(MyModelAdmin):
    list_display = ('short_name', 'name', 'display_index', 'created', 'modified')
    ordering = ['name']
admin.site.register(AliquotMedium,AliquotMediumAdmin)


class AliquotTypeAdmin(MyModelAdmin):

    list_display = ('alpha_code', 'numeric_code', 'name', 'created', 'modified')
    ordering = ['name']
    
admin.site.register(AliquotType,AliquotTypeAdmin)

class AliquotConditionAdmin(MyModelAdmin):
    list_display = ('display_index', 'name', 'short_name', 'field_name', 'created', 'modified')
    ordering = ['display_index']
admin.site.register(AliquotCondition,AliquotConditionAdmin)

class AliquotAdmin(MyModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            aliquot_identifier = AllocateAliquotIdentifier(
                request.user, 
                request.POST.get('aliquot_type'),
                )
            obj.aliquot_identifier = aliquot_identifier['id']
            obj.id_int = aliquot_identifier['id_int']
            obj.id_seed = aliquot_identifier['id_seed']
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

#unregistered admin_models

class AliquotInlineAdmin(MyTabularInline):
    
    model = Aliquot
    extra = 0

class ReceiveAdmin(AutocompleteAdmin, MyModelAdmin):
    
    def save_model(self, request, obj, form, change):
        if not change:

            receive_identifier = AllocateReceiveIdentifier(
                request.user, 
                )

            obj.receive_identifier = receive_identifier['id']

        save = super(ReceiveAdmin, self).save_model(request, obj, form, change)

        return save

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
