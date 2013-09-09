from django.db import models
from bhp_base_model.models import BaseModel

class BaseReport(BaseModel):
    
    report_name = models.CharField(
        verbose_name=("report name"),
        max_length=25,
        unique=True,
        )
    
    def __unicode__(self):
        return '{0}'.format(
            self.report_name)
    
    class Meta:
        app_label = 'bhp_birt_reports'