from django.db import models
from bhp_common.models import MyBasicUuidModel
from bhp_lab.models import Order

class Result(MyBasicUuidModel):
    order = models.ForeignKey(Order)
    
    class Meta:
        app_label = 'bhp_lab'    

class ResultItem(MyBasicUuidModel):
    result = models.ForeignKey(Result)
    
    class Meta:
        app_label = 'bhp_lab'    
