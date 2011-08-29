from django.db import models
from bhp_common.models import MyBasicModel
from panel import Panel


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
        app_label = 'bhp_lab_panel'        
        db_table = 'bhp_lab_core_tidpanelmapping'
