from django.db import models
from bhp_base_model.classes import BaseUuidModel


class ZplTemplate(BaseUuidModel):

    name = models.CharField(max_length=50)

    template = models.TextField(max_length=250)

    default = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'lab_barcode'
