from django.db import models
from bhp_base_model.models import BaseUuidModel


class ZplTemplate(BaseUuidModel):

    name = models.CharField(max_length=50)

    template = models.TextField(max_length=250)

    default = models.BooleanField(default=False)

    objects = models.Manager()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.default:
            # set others to False
            self.__class__.objects.all().update(default=False)
        super(ZplTemplate, self).save(*args, **kwargs)

    class Meta:
        app_label = 'lab_barcode'
