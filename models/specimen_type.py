from django.db import models
from bhp_common.models import MyBasicListModel

class SpecimenType (MyBasicListModel):
    pass
    
    class Meta:
        app_label = 'bhp_lab_core'
