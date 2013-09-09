from django.db import models
from bhp_base_model.models import BaseModel


class BaseSequence(BaseModel):

    device_id = models.IntegerField(default=99)
    objects = models.Manager()

    def __unicode(self):
        return self.pk

    class Meta:
        abstract = True
