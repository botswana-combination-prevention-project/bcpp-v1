from django.db import models
from bhp_common.models import MyBasicModel
from bhp_lab_core.models import TestCode, AliquotType
from bhp_lab_registration.models import Account

class PanelGroup (MyBasicModel):

    name = models.CharField(
        verbose_name = "Panel Group Name", 
        max_length=25,  
        unique=True,
        )

    def __unicode__(self):
        return self.name
        
    class Meta:
        app_label = 'bhp_lab_core'        


class Panel(MyBasicModel):
    
    name = models.CharField(
        verbose_name = "Panel Name", 
        max_length=50,  
        unique=True,
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
        app_label = 'bhp_lab_core'        


class TidPanelMapping(MyBasicModel):
    
    tid = models.CharField(
        verbose_name = 'dmis TID',
        max_length=3,
        )
        
    panel = models.ForeignKey(Panel)

    def __unicode__(self):
        return '%s->%s' % (self.tid, self.panel)
        
    class Meta:
        unique_together=(('tid','panel'),)
        app_label = 'bhp_lab_core'        

