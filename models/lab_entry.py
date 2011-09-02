from django.db import models
from bhp_common.models import MyBasicListModel, MyBasicUuidModel
from bhp_content_type_map.models import ContentTypeMap
from bhp_common.choices import YES_NO
from bhp_visit.models import BaseWindowPeriodItem, VisitDefinition
from lab_panel.models import Panel
from bhp_entry.choices import ENTRY_CATEGORY, ENTRY_WINDOW, ENTRY_STATUS

class LabEntry(BaseWindowPeriodItem):

    """Model of metadata for each model_class linked to a visit definition.
    
    This model lists entry forms by visit definition used to fill 
    the scheduled entry bucket for a subject once a visit is reported 
    
    Important: Read notes on model bhp_common.models ContentTypeMap
    """

    visit_definition = models.ForeignKey(VisitDefinition)
       
    panel = models.ForeignKey(Panel)
    
    entry_order = models.IntegerField()
    
    required = models.CharField(
        max_length = 10,
        choices = YES_NO,
        default = 'YES',
        )

    entry_category = models.CharField(
        max_length = 25,
        choices = ENTRY_CATEGORY,
        default = 'CLINIC',
        )    

    entry_window_calculation = models.CharField(
        max_length = 25,
        choices = ENTRY_WINDOW,
        default = 'VISIT',
        help_text = 'Base the entry window period on the visit window period or specify a form specific window period', 
        )    

    default_entry_status = models.CharField(
        max_length = 25,
        choices = ENTRY_STATUS,
        default = 'NEW',
        ) 
    
    def form_title(self):
        self.content_type_map.content_type.model_class()._meta.verbose_name
    
    def __unicode__(self):        
        return '%s: %s' % (self.visit_definition.code, self.panel.name)
   
    class Meta:
        app_label = 'bhp_lab_entry'
        verbose_name = "Lab Entry"
        ordering = ['visit_definition__code', 'entry_order',]
        unique_together = ['visit_definition', 'panel', ]   
