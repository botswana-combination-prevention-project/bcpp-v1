from django.db import models
from bhp_common.models import MyBasicModel
from lab_account.models import Account
from lab_test_code.models import TestCode
from lab_aliquot_list.models import AliquotType
from panel_group import PanelGroup


class Panel(MyBasicModel):
    
    name = models.CharField(
        verbose_name = "Panel Name", 
        max_length=50,  
        unique=True,
        db_index=True,                
        )

    panel_group = models.ForeignKey(PanelGroup)
        
    test_code = models.ManyToManyField(TestCode,
        verbose_name='Test Codes',
        help_text = 'Choose all that apply',
        )        

    aliquot_type = models.ManyToManyField(AliquotType,
        help_text = 'Choose all that apply',
        )        

    account = models.ManyToManyField(Account)
        
    comment = models.CharField(
        verbose_name = "Comment", 
        max_length=250, 
        blank=True,
        )
    dmis_panel_identifier = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        )    

    def __unicode__(self):
        return self.name
        
    class Meta:
        app_label = 'lab_panel'        
        db_table = 'bhp_lab_core_panel'



