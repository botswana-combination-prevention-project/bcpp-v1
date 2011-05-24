from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from bhp_common.validators import datetime_not_future, datetime_is_future
from bhp_common.choices import YES_NO
from bhp_employee.models import BaseEmployee

class PrincipalInvestigator (BaseEmployee):
    
    pass
    
    def get_absolute_url(self):
        return "/bhp_lab_registration/principalinvestigator/%s/" % self.id   
    
    class Meta(Employee.Meta):
        app_label = 'bhp_research_protocol'
