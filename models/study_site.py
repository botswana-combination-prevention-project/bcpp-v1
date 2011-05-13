from django.db import models
from django.utils.translation import ugettext_lazy as _
from bhp_common.models import MyBasicUuidModel


class StudySite(MyBasicUuidModel):
    
    site_code = models.CharField(max_length=4)        
    
    site_name = models.CharField(max_length=35)    
    
    def __unicode__(self):
        return "%s %s" % (self.site_code, self.site_name)
        
    class Meta:
        unique_together = [('site_code', 'site_name')]   
        ordering = ['site_code',] 
        app_label='bhp_variables'
        
