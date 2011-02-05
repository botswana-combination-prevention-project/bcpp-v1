from django.contrib import admin
from bhp_admin_models.models import MyModelAdmin, MyStackedInline
from models import Panel, Test, Aliquot, AliquotType, AliquotCondition
from models import Result, Order, ResultItem
from views import AllocateAliquotIdentifier

class TestInline(admin.TabularInline):
    model = Test
    extra = 5

class PanelAdmin(MyModelAdmin):
    inlines = [TestInline]
    list_display = ('name',)
admin.site.register(Panel, PanelAdmin)

class ResultAdmin(MyModelAdmin):
    pass
admin.site.register(Result, ResultAdmin)

class ResultItemAdmin(MyModelAdmin):
    pass
admin.site.register(ResultItem, ResultItemAdmin)

class OrderAdmin(MyModelAdmin):
    pass
admin.site.register(Order, OrderAdmin)

class AliquotTypeAdmin(MyModelAdmin):
    list_display = ('display_index', 'name', 'short_name', 'field_name', 'created', 'modified')
    ordering = ['display_index']
admin.site.register(AliquotType,AliquotTypeAdmin)

class AliquotConditionAdmin(MyModelAdmin):
    list_display = ('display_index', 'name', 'short_name', 'field_name', 'created', 'modified')
    ordering = ['display_index']
admin.site.register(AliquotCondition,AliquotConditionAdmin)

class AliquotAdmin(MyModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            aliquot_identifier = AllocateAliquotIdentifier(request.user, 
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
    list_display = ('aliquot_identifier', 'aliquot_volume', 'aliquot_type', 'aliquot_condition')        
    readonly_fields = ('aliquot_identifier',)        
admin.site.register(Aliquot, AliquotAdmin)    

#unregistered admin_models

class ReceiveAdmin(MyModelAdmin):
    def get_readonly_fields(self, request, obj = None):
        if obj: #In edit mode
            return ('aliquot',) + self.readonly_fields
        else:
            return self.readonly_fields     

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "aliquot":
            kwargs["queryset"] = Aliquot.objects.filter(receive__isnull=True)
        return super(ReceiveAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)   
            
    list_display = ('aliquot', 'subject_consent', 'datetime_drawn', 'datetime_received')        
#admin.site.register(Receive, ReceiveAdmin)    
