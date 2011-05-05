from django.db import models
from bhp_lab_reference.models import BaseReferenceList

class TestCodeReferenceList(BaseReferenceList):
    
    class Meta:
        app_label = 'bhp_lab_test_code'  
        ordering = ['name']   
