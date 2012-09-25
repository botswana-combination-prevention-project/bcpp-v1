from django.db import models
from bhp_base_model.classes import BaseModel


class Sequence(BaseModel):

    objects = models.Manager()

    def __unicode(self):
        return self.pk

    class Meta:
        app_label = "bhp_identifier"
        ordering = ['id', ]
