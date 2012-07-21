from django.db import models

from bhp_base_model.classes import BaseUuidModel

from zpl_template import ZplTemplate


class TestLabel(BaseUuidModel):

    identifier = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        )

    def label_template(self):
        zpl_template = ZplTemplate.objects.create(
            name='test_label',
            template=('^XA\n'
                '^FO325,5^A0N,15,20^FD${label_count}/${label_count_total}^FS\n'
                '^FO320,20^BY1,3.0^BCN,50,N,N,N\n'
                '^BY^FD${barcode_value}^FS\n'
                '^FO320,80^A0N,15,20^FD${barcode_value}^FS\n'
                '^FO325,152^A0N,20^FD${timestamp}^FS\n'
                '^XZ'))
        return zpl_template

    def barcode_value(self):
        return self.identifier

    def __unicode__(self):
        return self.identifier

    class Meta:
        app_label = 'lab_barcode'
        ordering = ['-created', ]
