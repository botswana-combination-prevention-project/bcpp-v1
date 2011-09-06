from bhp_common.models import MyModelAdmin
from lab_panel.models import Panel

class BaseRequisitionModelAdmin(MyModelAdmin):
    
    #override, limit dropdown in add_view to id passed in the URL        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        panel = request.GET.get('panel')
        if db_field.name == 'aliquot_type':
            if Panel.objects.filter(pk=panel):
                kwargs["queryset"] = Panel.objects.filter(pk=panel)
            
        return super(BaseRequisitionModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)   

