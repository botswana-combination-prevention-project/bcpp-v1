from django.db import models
from bhp_common.models import MyBasicListModel

class SpecimenType (MyBasicListModel):
    pass
    
    class Meta:
        app_label = 'lab_aliquot'
        db_table = 'bhp_lab_core_specimentype'
