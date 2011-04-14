from django.db import models
from bhp_common.models import MyBasicModel
from bhp_lab_core.models import TestCode

class Panel(MyBasicModel):
    
    name = models.CharField(
        verbose_name = "Panel Name", 
        max_length=25,  
        )
        
    test_code = models.ManyToManyField(TestCode,
        help_text = 'Choose all that apply',
        )        

    comment = models.CharField(
        verbose_name = "Comment", 
        max_length=250, 
        blank=True,
        )

    def __unicode__(self):
        return self.name
        
    class Meta:
        app_label = 'bhp_lab'        


