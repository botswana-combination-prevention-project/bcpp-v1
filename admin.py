from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline, MyTabularInline
from models import Panel, TestCode, Aliquot, AliquotType, AliquotCondition
from models import Receive, Result, Order, ResultItem, TestGroup, TestMap, AliquotMedium, TidPanelMapping, PanelGroup
from utils import AllocateAliquotIdentifier, AllocateReceiveIdentifier


class PanelAdmin(MyModelAdmin):
    list_display = ('name',)
admin.site.register(Panel, PanelAdmin)

class PanelGroupAdmin(MyModelAdmin):
    list_display = ('name',)
admin.site.register(PanelGroup, PanelGroupAdmin)

class TidPanelMappingAdmin(MyModelAdmin):
    list_display = ('tid','panel')
admin.site.register(TidPanelMapping, TidPanelMappingAdmin)

class TestCodeAdmin(MyModelAdmin):
    pass
admin.site.register(TestCode, TestCodeAdmin)

class TestMapAdmin(MyModelAdmin):
    pass
admin.site.register(TestMap, TestMapAdmin)

class TestGroupAdmin(MyModelAdmin):
    pass
admin.site.register(TestGroup, TestGroupAdmin)

class ResultItemAdmin(MyModelAdmin):
    pass
admin.site.register(ResultItem, ResultItemAdmin)


class ResultItemInlineAdmin(MyTabularInline):
    extra=2
    model = ResultItem

class ResultAdmin(MyModelAdmin):
    fields = ('order', 'result_datetime', 'assay_datetime', 'analyzer', 'source', 'archive', 'comment')
    inlines = [ResultItemInlineAdmin]
admin.site.register(Result, ResultAdmin)


class OrderAdmin(MyModelAdmin):
    pass
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
            return ('aliquot_type',) + self.readonly_fields
        else:
            return self.readonly_fields     
    list_display = ('aliquot_identifier', 'aliquot_type', 'measure', 'measure_units', 'condition', 'receive')        
    readonly_fields = ('aliquot_identifier',)        
admin.site.register(Aliquot, AliquotAdmin)    

#unregistered admin_models

class AliquotInlineAdmin(MyTabularInline):
    
    model = Aliquot
    extra = 1

class ReceiveAdmin(MyModelAdmin):
    
    def save_model(self, request, obj, form, change):
        if not change:

            receive_identifier = AllocateReceiveIdentifier(
                request.user, 
                )

            obj.receive_identifier = receive_identifier['id']

        save = super(ReceiveAdmin, self).save_model(request, obj, form, change)

        return save
            
    list_display = ('patient', 'datetime_drawn', 'datetime_received')        
    
    inlines = [AliquotInlineAdmin]

admin.site.register(Receive, ReceiveAdmin)    
