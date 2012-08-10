from django.db import models
from bhp_base_model.classes import BaseModel


class BasePanel(BaseModel):

    name = models.CharField(
        verbose_name="Panel Name",
        max_length=50,
        unique=True,
        db_index=True,
        )

    comment = models.CharField(
        verbose_name="Comment",
        max_length=250,
        blank=True,
        )

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
