from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline, MyTabularInline
from models import Panel, TestCode, Aliquot, AliquotType, AliquotCondition
from models import Receive, Result, Order, ResultItem, TestCodeGroup, TestCodeInterfaceMapping, AliquotMedium, TidPanelMapping, PanelGroup, ResultSource
from utils import AllocateAliquotIdentifier, AllocateReceiveIdentifier


class PanelAdmin(MyModelAdmin):
    list_display = ('name','panel_group')
admin.site.register(Panel, PanelAdmin)

class PanelGroupAdmin(MyModelAdmin):
    list_display = ('name',)
admin.site.register(PanelGroup, PanelGroupAdmin)

class TidPanelMappingAdmin(MyModelAdmin):
    list_display = ('tid','panel')
admin.site.register(TidPanelMapping, TidPanelMappingAdmin)

class TestCodeAdmin(MyModelAdmin):
    list_display = ('code', 'name', 'test_code_group', 'units', 'display_decimal_places', 'reference_range_lo', 'reference_range_hi', 'lln', 'uln')
admin.site.register(TestCode, TestCodeAdmin)

class TestCodeInterfaceMappingAdmin(MyModelAdmin):
    pass
admin.site.register(TestCodeInterfaceMapping, TestCodeInterfaceMappingAdmin)

class TestCodeGroupAdmin(MyModelAdmin):
    pass
admin.site.register(TestCodeGroup, TestCodeGroupAdmin)

class ResultItemAdmin(MyModelAdmin):
    pass
admin.site.register(ResultItem, ResultItemAdmin)


class ResultItemInlineAdmin(MyTabularInline):
    extra=0
    model = ResultItem

class ResultSourceAdmin(MyModelAdmin):
    pass
admin.site.register(ResultSource, ResultSourceAdmin)    

class ResultAdmin(MyModelAdmin):

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

        result = Result.objects.get(id__exact=object_id)
        
        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
            response['Location'] = result.get_search_url()
        return response
    
    fields = ('order', 'result_datetime', 'assay_datetime', 'result_source', 'result_source_reference', 'comment')
    inlines = [ResultItemInlineAdmin]
    
admin.site.register(Result, ResultAdmin)


class OrderAdmin(MyModelAdmin):
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

class ReceiveAdmin(MyModelAdmin):
    
    def save_model(self, request, obj, form, change):
        if not change:

            receive_identifier = AllocateReceiveIdentifier(
                request.user, 
                )

            obj.receive_identifier = receive_identifier['id']

        save = super(ReceiveAdmin, self).save_model(request, obj, form, change)

        return save
            
    list_display = ('patient', 'datetime_drawn', 'receive_datetime')        
    
    inlines = [AliquotInlineAdmin]

admin.site.register(Receive, ReceiveAdmin)    
