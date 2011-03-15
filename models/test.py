from django.db import models
from bhp_common.models import MyBasicModel

class Test(MyBasicModel):
    
    test_code = models.CharField(
        verbose_name = "Univeral Test ID", 
        max_length=10, 
        unique=True
        )
    test_name = models.CharField(
        verbose_name = "UTestID Description", 
        max_length=25
        )
    comment = models.CharField(
        verbose_name = "Comment", 
        max_length=250, 
        blank=True
        )

    def __unicode__(self):
        return "%s: %s" % (self.test_code,self.test_name)
        
    class Meta:
        app_label = 'bhp_lab'        
