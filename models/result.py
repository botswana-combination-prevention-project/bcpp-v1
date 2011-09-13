from django.db import models
from django.utils.translation import ugettext_lazy as _
from lab_result.models.base_result import BaseResult
from lab_clinic_api.managers import ResultManager
from lab_clinic_api.models import Lab

class Result(BaseResult):

    lab = models.ForeignKey(Lab)
    
    objects = ResultManager()
    
    def __unicode__(self):
        return '%s' % (self.result_identifier)

    def get_absolute_url(self):
        return "/lab_clinic_api/result/%s/" % self.id   
        
    class Meta:
        app_label = 'lab_clinic_api' 
        #ordering =['result_identifier']      
