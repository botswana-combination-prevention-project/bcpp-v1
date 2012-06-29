from django.contrib import admin
from bhp_common.models import MyModelAdmin
from lab_panel.models import Panel
from bhp_lab_entry.models import ScheduledLabEntryBucket
from bhp_visit_tracking.classes import VisitModelHelper
from lab_barcode.actions import print_barcode_labels
from lab_requisition.actions import flag_as_received, flag_as_not_received, flag_as_not_labelled


class BaseRequisitionModelAdmin(MyModelAdmin):

    actions = [flag_as_received, 
                        flag_as_not_received, 
                        flag_as_not_labelled, 
                        print_barcode_labels]
    
    def __init__(self, *args, **kwargs):

        self.fields = [
            self.visit_fieldname,
            "requisition_datetime",
            "is_drawn",
            "reason_not_drawn",
            "drawn_datetime",
            "site",
            "panel",
            "aliquot_type",                
            "item_type",
            "item_count_total",
            "estimated_volume",
            "priority",
            #"test_code",        
            #"clinician_initials",
            "comments",]

        self.radio_fields = {
            "is_drawn":admin.VERTICAL,
            "reason_not_drawn":admin.VERTICAL,                        
            "item_type":admin.VERTICAL,                
            "priority":admin.VERTICAL,
            "site":admin.VERTICAL,        
            }
        
        self.list_display = [
            'requisition_identifier',
            'specimen_identifier',
            self.visit_fieldname,
            "requisition_datetime",
            "panel",
            'hostname_created', 
            "priority",
            'is_receive',
            'is_labelled',
            'is_packed', 
            'is_lis',
            'is_receive_datetime',
            'is_labelled_datetime',              
            #'packing_list',
            ]        

        self.list_filter = [
            "priority",
            'is_receive',
            'is_labelled',
            'is_packed', 
            'is_lis',
            "requisition_datetime",
            'is_receive_datetime',
            'is_labelled_datetime',            
            'hostname_created']
        
        self.search_fields = [
            '%s__appointment__registered_subject__subject_identifier' % (self.visit_fieldname,),
            'specimen_identifier',
            'requisition_identifier']

        
        
        super(BaseRequisitionModelAdmin, self).__init__(*args, **kwargs)

    
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
        
    def save_model(self, request, obj, form, change):
        
        if not self.visit_model:
            raise AttributeError, 'visit_model cannot be None. Specify in the ModelAdmin class. e.g. visit_model = \'maternal_visit\''            
        
        ScheduledLabEntryBucket.objects.update_status(
            model_instance = obj,
            visit_model = self.visit_model,
            )
                        
        return super(BaseRequisitionModelAdmin, self).save_model(request, obj, form, change)
        
    def delete_model(self, request, obj):

        if not self.visit_model:
            raise AttributeError, 'delete_model(): visit_model cannot be None. Specify in the ModelAdmin class. e.g. visit_model = \'maternal_visit\''            

        ScheduledLabEntryBucket.objects.update_status(
            model_instance = obj,
            visit_model = self.visit_model,
            action = 'delete',
            )

        return super(BaseRequisitionModelAdmin, self).delete_model(request, obj) 
