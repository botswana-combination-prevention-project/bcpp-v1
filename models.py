from django.db import models
from bhp_basic_models.models import MyBasicModel

class MyCodeList (MyBasicModel):
    code = models.CharField("Code",
        max_length=15,
        unique=True)
    short_name = models.CharField("Name",
        max_length=35)    
    long_name = models.CharField("Long Name",
        max_length=255,
        blank=True)    
    
    class Meta:
        abstract=True

#dx and ssx        

class WhoClinicalStagingDxAdult(MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    

class WhoClinicalStagingDxPediatric(MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    

class DiagnosisCode (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    

class SignsSymptomsCode (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    

class MedicationCode (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    

class BodySiteCode (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    

class OrganismCode (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    

#ARV medications
class ArvCode (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    

class ArvDoseStatus (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    

class ArvModificationCode (MyCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)    
    
