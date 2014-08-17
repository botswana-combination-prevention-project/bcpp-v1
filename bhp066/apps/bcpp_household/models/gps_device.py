from django.db import models

from edc.base.model.models import BaseListModel

from ..managers import GpsDeviceManager


class GpsDevice(BaseListModel):

    gps_make = models.CharField("Make", max_length=25)
    gps_model = models.CharField("Model", max_length=25)
    gps_serial_number = models.CharField("Serial Number", max_length=25)
    gps_purchase_date = models.DateField("Purchase Date")
    gps_purchase_price = models.DecimalField("Purchase Price",
                                             max_digits=10,
                                             decimal_places=2)

    objects = GpsDeviceManager()

    def __unicode__(self):
        return "{0} {1} {2}".format(self.name, self.gps_make, self.gps_model)

#     def get_absolute_url(self):
#         return "/bcpp_household/gpsdevice/{0}/".format(self.id)

    def natural_key(self):
        return (self.gps_serial_number, )

    class Meta:
        app_label = 'bcpp_household'
