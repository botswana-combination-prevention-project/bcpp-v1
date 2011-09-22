from bhp_common.models import MyModelAdmin
from lab_panel.models import Panel

class BaseRequisitionModelAdmin(MyModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        panel_pk = request.GET.get('panel',0)
        if db_field.name == 'panel':
            kwargs["queryset"] = Panel.objects.filter(pk = panel_pk)                                                        
        if db_field.name == 'aliquot_type':
            if Panel.objects.filter(pk=panel_pk):
                kwargs["queryset"] = Panel.objects.get(pk=panel_pk).aliquot_type.all()
            
        return super(BaseRequisitionModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)   

