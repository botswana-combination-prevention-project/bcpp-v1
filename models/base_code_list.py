from django.db import models
from bhp_base_model.models import BaseModel


class BaseCodeList (BaseModel):

    code = models.CharField("Code",
        max_length=15,
        unique=True,
        )

    short_name = models.CharField("Name",
        max_length=35,
        )

    long_name = models.CharField("Long Name",
        max_length=255,
        blank=True,
        )

    def __unicode__(self):
        return "%s" % (self.short_name)

    class Meta:
        abstract = True
