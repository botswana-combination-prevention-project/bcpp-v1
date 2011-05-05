from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from bhp_common.models import MyBasicModel, MyBasicListModel
from bhp_lab_reference.models import BaseReferenceList

class GradingList(BaseReferenceList):

    class Meta:
        app_label = "bhp_grading"
        ordering = ['name']

