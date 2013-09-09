from django.db import models
from django.core.validators import RegexValidator
from bhp_base_model.models import BaseUuidModel


class Group(BaseUuidModel):

    name = models.CharField(
        max_length=5,
        validators=RegexValidator('[A-Z]{1,5}')
        )
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=250)
    probability = models.FloatField()
    objects = models.Manager()

    class Meta:
        app_label = 'bhp_supplemental_fields'
