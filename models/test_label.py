from django.db import models

from bhp_base_model.classes import BaseUuidModel


class TestLabel(BaseUuidModel):

    identifier = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        )

    def barcode_value(self):
        return self.identifier

    def __unicode__(self):
        return self.identifier

    #def save(self, *args, **kwargs):
    #    pass

    class Meta:
        app_label = 'lab_barcode'
        ordering = ['-created', ]
