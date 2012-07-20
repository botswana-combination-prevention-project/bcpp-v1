from django.db import models
from bhp_base_model.classes import BaseUuidModel


class LabelPrinter(BaseUuidModel):

    cups_printer_name = models.CharField(max_length=50)

    cups_server_ip = models.IPAddressField()

    default = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s@%s' % (self.cups_printer_name, self.cups_server_ip,)

    class Meta:
        app_label = 'lab_barcode'
        ordering = ['cups_server_ip', ]
