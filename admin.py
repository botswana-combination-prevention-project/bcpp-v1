from django.contrib import admin
from bhp_admin_models.models import MyModelAdmin, MyStackedInline
from models import Panel, Test, LabAliquot, LabReceive, LabAliquotType, LabAliquotCondition

class TestInline(admin.TabularInline):
    model = Test
    extra = 5
   
class PanelAdmin(MyModelAdmin):
    inlines = [TestInline]
    list_display = ('name',)

admin.site.register(Panel, PanelAdmin)

class LabAliquotTypeAdmin(MyModelAdmin):
    list_display = ('display_index', 'name', 'short_name', 'field_name', 'created', 'modified')
    ordering = ['display_index']
admin.site.register(LabAliquotType,LabAliquotTypeAdmin)

class LabAliquotConditionAdmin(MyModelAdmin):
    list_display = ('display_index', 'name', 'short_name', 'field_name', 'created', 'modified')
    ordering = ['display_index']
admin.site.register(LabAliquotCondition,LabAliquotConditionAdmin)

class LabAliquotAdmin(MyModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            aliquot_identifier = AllocateAliquotIdentifier(request.user, 
                request.POST.get('lab_aliquot_type'),
            )
            obj.aliquot_identifier = aliquot_identifier['id']
            obj.id_int = aliquot_identifier['id_int']
            obj.id_seed = aliquot_identifier['id_seed']
        save = super(LabAliquotAdmin, self).save_model(request, obj, form, change)
        return save

    def get_readonly_fields(self, request, obj = None):
        if obj: #In edit mode
            return ('lab_aliquot_type',) + self.readonly_fields
        else:
            return self.readonly_fields     
    list_display = ('aliquot_identifier', 'aliquot_volume', 'lab_aliquot_type', 'lab_aliquot_condition')        
    readonly_fields = ('aliquot_identifier',)        
admin.site.register(LabAliquot, LabAliquotAdmin)    

class LabReceiveAdmin(MyModelAdmin):
    def get_readonly_fields(self, request, obj = None):
        if obj: #In edit mode
            return ('lab_aliquot',) + self.readonly_fields
        else:
            return self.readonly_fields     

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "lab_aliquot":
            kwargs["queryset"] = LabAliquot.objects.filter(labreceive__isnull=True)
        return super(LabReceiveAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)   
            
    list_display = ('lab_aliquot', 'subject_consent', 'datetime_drawn', 'datetime_received')        
admin.site.register(LabReceive, LabReceiveAdmin)    
