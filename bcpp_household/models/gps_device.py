from django.db import models

from edc_base.model.models import ListModelMixin, BaseUuidModel

from ..managers import GpsDeviceManager


class GpsDevice(ListModelMixin, BaseUuidModel):
    """A system model that indicates the GPS device used to confirm a plot."""
    gps_make = models.CharField("Make", max_length=25)
    gps_model = models.CharField("Model", max_length=25)
    gps_serial_number = models.CharField("Serial Number", max_length=25)
    gps_purchase_date = models.DateField("Purchase Date")
    gps_purchase_price = models.DecimalField("Purchase Price",
                                             max_digits=10,
                                             decimal_places=2)

    objects = GpsDeviceManager()

    def __str__(self):
        return "{0} {1} {2}".format(self.name, self.gps_make, self.gps_model)

    def natural_key(self):
        return (self.gps_serial_number, )

    class Meta:
        app_label = 'bcpp_household'
