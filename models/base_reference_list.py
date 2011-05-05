from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from bhp_common.models import MyBasicModel, MyBasicListModel

class BaseReferenceList(MyBasicModel):

    name = models.CharField(
        verbose_name="List name",
        max_length = 25,
        )
    
    description = models.CharField(
        verbose_name="Description",
        max_length = 250,
        null=True,
        blank=True,
        )
    
    list_date = models.DateField(
        null=True,
        blank=True,
        )
        
    class Meta:
        abstract = True
        app_label = "bhp_grading"
        ordering = ['name']        
