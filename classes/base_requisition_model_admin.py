from bhp_common.models import MyModelAdmin
from lab_panel.models import Panel
from bhp_appointment.classes import BaseVisitModelAdmin
from bhp_appointment.classes import VisitModelHelper

class BaseRequisitionModelAdmin(MyModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        panel_pk = request.GET.get('panel',0)
        if db_field.name == 'panel':
            kwargs["queryset"] = Panel.objects.filter(pk = panel_pk)                                                        
        if db_field.name == 'aliquot_type':
            if Panel.objects.filter(pk=panel_pk):
                kwargs["queryset"] = Panel.objects.get(pk=panel_pk).aliquot_type.all()

        
        visit_model_helper = VisitModelHelper()
        if db_field.name == visit_model_helper.get_visit_field(model=self.model, visit_model=self.visit_model):
            kwargs["queryset"] = visit_model_helper.set_visit_queryset(
                                                            subject_identifier = request.GET.get('subject_identifier', 0),
                                                            visit_code = request.GET.get('visit_code', 0),
                                                            visit_instance = request.GET.get('visit_instance', 0),
                                                            )
            
        return super(BaseRequisitionModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)   

