from django.db import models


class GpsDeviceManager(models.Manager):

    def get_by_natural_key(self, gps_serial_number):
        return self.get(gps_serial_number=gps_serial_number)
