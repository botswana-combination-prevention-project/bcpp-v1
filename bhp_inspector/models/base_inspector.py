from bhp_base_model.models import BaseUuidModel
from django.db import models

class BaseInspector(BaseUuidModel):

    item_identifier = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        verbose_name = 'Item Identifier'
        )
    
    app_name = models.CharField(
        max_length=25,
        verbose_name = 'Application Name'
        )
    
    model_name = models.CharField(
        max_length=25,
        verbose_name = 'Model Name'
        )
    
    is_confirmed = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='Inspector confirmed'
        )
    
    class Meta:
        abstract = True
