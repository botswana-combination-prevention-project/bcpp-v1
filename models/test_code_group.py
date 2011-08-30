from django.db import models
from bhp_common.models import MyBasicModel
    
class TestCodeGroup(MyBasicModel):
    
    code = models.CharField(
        max_length=3
        )
    name = models.CharField(
        max_length = 25,
        null=True,
        blank=True,
        )
    
    def __unicode__(self):
        return self.code    
    class Meta:
        app_label = 'lab_test_code'
        db_table = 'bhp_lab_test_code_testcodegroup'
        ordering = ['code',]
