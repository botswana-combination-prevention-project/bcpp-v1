from django.db import models
from lab_base_model.models import BaseLabModel


class BasePanel(BaseLabModel):

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
