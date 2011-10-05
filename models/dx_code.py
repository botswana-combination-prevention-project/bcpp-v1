from django.db import models
from base_code_list import BaseCodeList

class DxCode (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    
    class Meta:
        app_label="bhp_code_lists"
