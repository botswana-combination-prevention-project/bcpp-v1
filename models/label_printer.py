from django.db import models
from bhp_base_model.classes import BaseUuidModel


class LabelPrinter(BaseUuidModel):

    cups_printer_name = models.CharField(max_length=50)

    cups_server_ip = models.IPAddressField()

    default = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s@%s' % (self.cups_printer_name, self.cups_server_ip,)

    def save(self, *args, **kwargs):
        if self.default:
            # set others to False
            self.__class__.objects.all().update(default=False)
        super(LabelPrinter, self).save(*args, **kwargs)

    class Meta:
        app_label = 'lab_barcode'
        ordering = ['cups_server_ip', ]
