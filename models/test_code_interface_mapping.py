from django.db import models
from bhp_common.models import MyBasicModel
from bhp_lab_test_code.models import TestCode

class TestCodeInterfaceMapping(MyBasicModel):

    foreign_test_code = models.CharField(
        verbose_name = "Foreign Test Code", 
        max_length=15, 
        unique=True,
        )
        
    local_test_code = models.ForeignKey(TestCode,
        verbose_name = "Local Test Code", 
        )

    def __unicode__(self):
        return "%s maps to %s" % (self.foreign_test_code,self.local_test_code)

    class Meta:
        app_label = 'bhp_lab_test_code'            

           
