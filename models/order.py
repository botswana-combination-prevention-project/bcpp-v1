from django.db import models
from bhp_common.models import MyBasicUuidModel
from bhp_lab.models import Aliquot

class Order(MyBasicUuidModel):
    aliquot = models.ForeignKey(Aliquot)    
