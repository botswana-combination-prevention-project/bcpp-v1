from django.db import models
from bhp_common.models import MyBasicUuidModel
from label_printer import LabelPrinter


class Client(MyBasicUuidModel):

    ip = models.IPAddressField()
    
    name = models.CharField(
        max_length = 50,
        null=True,
        blank=True,
        )

    label_printer = models.ForeignKey(LabelPrinter)

    def __unicode__(self):
        return "%s - %s" % (self.ip, self.name,)
        
    class Meta:
        app_label='lab_barcode'             

