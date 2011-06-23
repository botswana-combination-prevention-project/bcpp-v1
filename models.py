from django.db import models
from bhp_common.models import MyBasicModel

class MyCodeList (MyBasicModel):
    
    code = models.CharField("Code",
        max_length = 15,
        unique = True,
        )
    
    short_name = models.CharField("Name",
        max_length = 35,
        )    
    
    long_name = models.CharField("Long Name",
        max_length = 255,
        blank = True,
        )    
    
    class Meta:
        abstract = True

#dx and ssx        
class WcsDxAdult(MyCodeList):
    
    """WhoClinicalStagingDxAdult"""
    
    list_ref = models.CharField("List Reference",
        max_length = 35,
        blank = True,        
        )    

    class Meta:
        app_label = "bhp_code_lists"


class WcsDxPed(MyCodeList):
    
    """WhoClinicalStagingDxPediatric"""

    list_ref = models.CharField("List Reference",
        max_length = 35,
        blank = True,
        )    

    class Meta:
        app_label = "bhp_code_lists"


class DxCode (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    
    class Meta:
        app_label="bhp_code_lists"

class SsxCode (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    
    class Meta:
        app_label="bhp_code_lists"

class MedicationCode (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    
    class Meta:
        app_label="bhp_code_lists"

class BodySiteCode (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    
    class Meta:
        app_label="bhp_code_lists"

class OrganismCode (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    
    class Meta:
        app_label="bhp_code_lists"

#ARV medications
class ArvCode (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    
    class Meta:
        app_label="bhp_code_lists"

class ArvDoseStatus (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    
    class Meta:
        app_label="bhp_code_lists"

class ArvModificationCode (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    
    class Meta:
        app_label="bhp_code_lists"

