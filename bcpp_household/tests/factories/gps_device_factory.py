import factory
from datetime import date
from edc_lib.bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_household.models import GpsDevice


class GpsDeviceFactory(BaseUuidModelFactory):
    FACTORY_FOR = GpsDevice

    display_index = 2
    version = factory.Sequence(lambda n: 'version{0}'.format(n))
    gps_make = factory.Sequence(lambda n: 'gps_make{0}'.format(n))
    gps_model = factory.Sequence(lambda n: 'gps_model{0}'.format(n))
    gps_serial_number = factory.Sequence(lambda n: 'gps_serial_number{0}'.format(n))
    gps_purchase_date = date.today()
    gps_purchase_price = 2.5
