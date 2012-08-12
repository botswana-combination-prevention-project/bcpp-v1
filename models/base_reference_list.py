from django.db import models
from bhp_base_model.classes import BaseModel


class BaseReferenceList(BaseModel):

    name = models.CharField(
        verbose_name="List name",
        max_length=50,
        )

    description = models.CharField(
        verbose_name="Description",
        max_length=250,
        null=True,
        blank=True,
        )

    list_date = models.DateField(
        null=True,
        blank=True,
        )

    objects = models.Manager()

    class Meta:
        abstract = True
        app_label = "bhp_grading"
        ordering = ['name']
